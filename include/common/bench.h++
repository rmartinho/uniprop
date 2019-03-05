#pragma once

#include <common/general_category.h++>

#include <nonius.h++>

#include <vector>
#include <random>

#define MAKE_BENCH(NAMESPACE, CATEGORY)                         \
NONIUS_BENCHMARK(#NAMESPACE " [" #CATEGORY "]",                 \
[](nonius::chronometer meter) {                                 \
    std::vector<char32_t> chars(meter.runs());                  \
    std::vector<bool> results(meter.runs());                    \
                                                                \
    std::minstd_rand rng(0);                                    \
    std::uniform_int_distribution<char32_t> dist(0, 0x10FFFF);  \
                                                                \
    for(auto& c: chars) {                                       \
        do {                                                    \
            c = dist(rng);                                      \
        } while(c >= 0xD800 && c <= 0xDFFF);                    \
    }                                                           \
                                                                \
    meter.measure([&](int i) {                                  \
        results[i] = is<general_category::CATEGORY>(chars[i]);  \
    });                                                         \
})

#define MAKE_BENCHES(NAMESPACE) \
namespace NAMESPACE {           \
MAKE_BENCH(NAMESPACE, c)        \
MAKE_BENCH(NAMESPACE, cc)       \
MAKE_BENCH(NAMESPACE, cf)       \
MAKE_BENCH(NAMESPACE, cn)       \
MAKE_BENCH(NAMESPACE, co)       \
MAKE_BENCH(NAMESPACE, l)        \
MAKE_BENCH(NAMESPACE, ll)       \
MAKE_BENCH(NAMESPACE, lm)       \
MAKE_BENCH(NAMESPACE, lo)       \
MAKE_BENCH(NAMESPACE, lt)       \
MAKE_BENCH(NAMESPACE, lu)       \
MAKE_BENCH(NAMESPACE, m)        \
MAKE_BENCH(NAMESPACE, mc)       \
MAKE_BENCH(NAMESPACE, me)       \
MAKE_BENCH(NAMESPACE, mn)       \
MAKE_BENCH(NAMESPACE, n)        \
MAKE_BENCH(NAMESPACE, nd)       \
MAKE_BENCH(NAMESPACE, nl)       \
MAKE_BENCH(NAMESPACE, no)       \
MAKE_BENCH(NAMESPACE, p)        \
MAKE_BENCH(NAMESPACE, pc)       \
MAKE_BENCH(NAMESPACE, pd)       \
MAKE_BENCH(NAMESPACE, pe)       \
MAKE_BENCH(NAMESPACE, pf)       \
MAKE_BENCH(NAMESPACE, pi)       \
MAKE_BENCH(NAMESPACE, po)       \
MAKE_BENCH(NAMESPACE, ps)       \
MAKE_BENCH(NAMESPACE, sc)       \
MAKE_BENCH(NAMESPACE, sk)       \
MAKE_BENCH(NAMESPACE, sm)       \
MAKE_BENCH(NAMESPACE, so)       \
MAKE_BENCH(NAMESPACE, z)        \
MAKE_BENCH(NAMESPACE, zl)       \
MAKE_BENCH(NAMESPACE, zp)       \
MAKE_BENCH(NAMESPACE, zs)       \
}
