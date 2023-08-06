// Copyright (C) 2022-2023 Exaloop Inc. <https://exaloop.io>

#pragma once

#include "llvm/Support/Path.h"
#include <chrono>
#include <fmt/format.h>
#include <fmt/ostream.h>
#include <fmt/ranges.h>
#include <fmt/std.h>
#include <iostream>
#include <ostream>

#include "codon/compiler/error.h"
#include "codon/config/config.h"
#include "codon/parser/ast/error.h"

#pragma clang diagnostic push
#pragma clang diagnostic ignored "-Wgnu-zero-variadic-macro-arguments"
static std::string get_file_name(const char *path) {
  return llvm::sys::path::filename(path).str();
}

#define DBG(c, ...)                                                                    \
  fmt::print(codon::getLogger().log, "{} {} {} " c "\n",                                      \
             std::string(2 * codon::getLogger().level, ' '), get_file_name(__FILE__), __LINE__, ##__VA_ARGS__)
#define LOG(c, ...) DBG(c, ##__VA_ARGS__)
#define LOG_TIME(c, ...)                                                               \
  {                                                                                    \
    if (codon::getLogger().flags & codon::Logger::FLAG_TIME)                           \
      DBG(c, ##__VA_ARGS__);                                                           \
  }
#define LOG_REALIZE(c, ...)                                                            \
  {                                                                                    \
    if (codon::getLogger().flags & codon::Logger::FLAG_REALIZE)                        \
      DBG(c, ##__VA_ARGS__);                                                           \
  }
#define LOG_TYPECHECK(c, ...)                                                          \
  {                                                                                    \
    if (codon::getLogger().flags & codon::Logger::FLAG_TYPECHECK)                      \
      DBG(c, ##__VA_ARGS__);                                                           \
  }
#define LOG_IR(c, ...)                                                                 \
  {                                                                                    \
    if (codon::getLogger().flags & codon::Logger::FLAG_IR)                             \
      DBG(c, ##__VA_ARGS__);                                                           \
  }
#define LOG_USER(c, ...)                                                               \
  {                                                                                    \
    if (codon::getLogger().flags & codon::Logger::FLAG_USER)                           \
      DBG(c, ##__VA_ARGS__);                                                           \
  }

#define TIME(name) codon::Timer __timer(name)

#ifndef NDEBUG
#define seqassertn(expr, msg, ...)                                                     \
  ((expr) ? (void)(0)                                                                  \
          : codon::assertionFailure(#expr, __FILE__, __LINE__,                         \
                                    fmt::format(msg, ##__VA_ARGS__)))
#define seqassert(expr, msg, ...)                                                      \
  ((expr) ? (void)(0)                                                                  \
          : codon::assertionFailure(                                                   \
                #expr, __FILE__, __LINE__,                                             \
                fmt::format(msg " [{}]", ##__VA_ARGS__, getSrcInfo())))
#else
#define seqassertn(expr, msg, ...) ;
#define seqassert(expr, msg, ...) ;
#endif
#pragma clang diagnostic pop

namespace codon {

void assertionFailure(const char *expr_str, const char *file, int line,
                      const std::string &msg);

struct Logger {
  static constexpr int FLAG_TIME = (1 << 0);
  static constexpr int FLAG_REALIZE = (1 << 1);
  static constexpr int FLAG_TYPECHECK = (1 << 2);
  static constexpr int FLAG_IR = (1 << 3);
  static constexpr int FLAG_USER = (1 << 4);

  int flags;
  int level;
  std::ostream &out;
  std::ostream &err;
  std::ostream &log;

  Logger() : flags(0), level(0), out(std::cout), err(std::cerr), log(std::clog) {}

  void parse(const std::string &logs);
};

Logger &getLogger();
void pushLogger();
bool popLogger();

class Timer {
private:
  using clock_type = std::chrono::high_resolution_clock;
  std::string name;
  std::chrono::time_point<clock_type> start, end;

public:
  bool logged;

public:
  void log() {
    if (!logged) {
      LOG_TIME("[T] {} = {:.3f}", name, elapsed());
      logged = true;
    }
  }

  double elapsed(std::chrono::time_point<clock_type> end = clock_type::now()) const {
    return std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count() /
           1000.0;
  }

  Timer(std::string name) : name(std::move(name)), start(), end(), logged(false) {
    start = clock_type::now();
  }

  ~Timer() { log(); }
};

std::ostream &operator<<(std::ostream &out, const codon::SrcInfo &src);

struct SrcObject {
private:
  SrcInfo info;

public:
  SrcObject() : info() {}
  SrcObject(const SrcObject &s) { setSrcInfo(s.getSrcInfo()); }

  virtual ~SrcObject() = default;

  SrcInfo getSrcInfo() const { return info; }

  void setSrcInfo(SrcInfo info) { this->info = std::move(info); }
};
template <class... TA> void E(error::Error e, codon::SrcObject *o, const TA &...args) {
  E(e, o->getSrcInfo(), args...);
}
template <class... TA>
void E(error::Error e, const codon::SrcObject &o, const TA &...args) {
  E(e, o.getSrcInfo(), args...);
}
template <class... TA>
void E(error::Error e, const std::shared_ptr<SrcObject> &o, const TA &...args) {
  E(e, o->getSrcInfo(), args...);
}

enum MessageGroupPos {
  NONE = 0,
  HEAD,
  MID,
  LAST,
};

void compilationError(const std::string &msg, const std::string &file = "",
                      int line = 0, int col = 0, int len = 0, int erroCode = -1,
                      bool terminate = true, MessageGroupPos pos = NONE);

void compilationWarning(const std::string &msg, const std::string &file = "",
                        int line = 0, int col = 0, int len = 0, int erroCode = -1,
                        bool terminate = false, MessageGroupPos pos = NONE);

} // namespace codon

template <> struct fmt::formatter<codon::SrcInfo> : fmt::ostream_formatter {};

//borrow from cdt/libraries/eosiolib/core/eosio/name.hpp

constexpr uint8_t name_length(uint64_t value) {
    constexpr uint64_t mask = 0xF800000000000000ull;

    if( value == 0 )
      return 0;

    uint8_t l = 0;
    uint8_t i = 0;
    for( auto v = value; i < 13; ++i, v <<= 5 ) {
      if( (v & mask) > 0 ) {
          l = i;
      }
    }

    return l + 1;
}

static char* _n2s(uint64_t value, char* begin, char* end, bool dry_run = false ) {
    static const char* charmap = ".12345abcdefghijklmnopqrstuvwxyz";
    constexpr uint64_t mask = 0xF800000000000000ull;

    if( dry_run || (begin + 13 < begin) || (begin + 13 > end) ) {
      char* actual_end = begin + name_length(value);
      if( dry_run || (actual_end < begin) || (actual_end > end) ) return actual_end;
    }

    auto v = value;
    for( auto i = 0; i < 13; ++i, v <<= 5 ) {
      if( v == 0 ) return begin;

      auto indx = (v & mask) >> (i == 12 ? 60 : 59);
      *begin = charmap[indx];
      ++begin;
    }

    return begin;
}

static std::string n2s(uint64_t value) {
    char buffer[13];
    auto end = _n2s(value, buffer, buffer + sizeof(buffer) );
    return {buffer, end};
}

inline constexpr uint64_t char_to_symbol( char c ) {
  if( c >= 'a' && c <= 'z' )
      return (c - 'a') + 6;
  if( c >= '1' && c <= '5' )
      return (c - '1') + 1;
  return 0;
}

inline constexpr uint64_t s2n( std::string_view str ) {
  uint64_t n = 0;
  size_t i = 0;
  for ( ; i < str.size() && i < 12; ++i) {
      // NOTE: char_to_symbol() returns char type, and without this explicit
      // expansion to uint64 type, the compilation fails at the point of usage
      // of string_to_name(), where the usage requires constant (compile time) expression.
      n |= (char_to_symbol(str[i]) & 0x1f) << (64 - 5 * (i + 1));
  }

  // The for-loop encoded up to 60 high bits into uint64 'name' variable,
  // if (strlen(str) > 12) then encode str[12] into the low (remaining)
  // 4 bits of 'name'
  if (i < str.size() && i == 12)
      n |= char_to_symbol(str[12]) & 0x0F;
  return n;
}

static inline bool verify_name( std::string_view str ) {
  if( str.size() > 13 ) return false;

  for( size_t i = 0; i < str.size(); ++i ) {
      auto c = char_to_symbol(str[i]);
      if( c == 0 && str[i] != '.' ) return false;
  }

  return true;
}
