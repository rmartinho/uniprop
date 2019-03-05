#pragma once

#include <booltrie/structs.h++>

#include <array>
#include <initializer_list>
#include <cstdint>
#include <immintrin.h>

namespace sg16 {

struct exhaustive_list16_avx {
    constexpr std::size_t size() const noexcept {
        return full_size(list);
    }

    constexpr bool operator()(char32_t u) const noexcept {
        if (u > 0xFFFF) {
            return false;
        }

        auto u16 = static_cast<std::uint16_t>(u);
        auto needle = _mm256_set1_epi16(u16);
        for(auto ptr = list.begin(); ptr != list.end(); ptr += 16) {
            auto haystack = _mm256_loadu_si256(reinterpret_cast<__m256i const*>(ptr));
            auto eq = _mm256_cmpeq_epi16(needle, haystack);
            if (!_mm256_testz_si256(eq, eq)) {
                return true;
            }
        }
        return false;
    }

    std::initializer_list<std::uint16_t> list;
};

}
