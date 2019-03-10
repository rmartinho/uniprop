#pragma once

#include <array>
#include <initializer_list>
#include <iterator>
#include <algorithm>
#include <cstdint>

namespace sg16 {

constexpr bool trie_range_leaf(std::uint32_t c, std::uint64_t chunk) noexcept {
    return (chunk >> (c & 0b111111)) & 0b1;
}

template <typename T>
constexpr std::size_t full_size(std::initializer_list<T> l) noexcept {
    return sizeof(l) + l.size() * sizeof(decltype(*l.begin()));
}

struct bool_trie {
    // 0..0x800
    std::array<std::uint64_t, 32> r1;

    // 0x800..0x10000
    std::array<std::uint8_t, 992> r2;
    std::initializer_list<std::uint64_t> r3;

    // 0x10000..0x110000
    std::array<std::uint8_t, 256> r4;
    std::initializer_list<std::uint8_t> r5;
    std::initializer_list<std::uint64_t> r6;
    
    constexpr std::size_t size() const noexcept {
        return sizeof(r1) + sizeof(r2) + full_size(r3)
             + sizeof(r4) + full_size(r5) + full_size(r6);
    }

    constexpr bool operator()(char32_t u) const noexcept {
        auto c = static_cast<std::uint32_t>(u);
        if (c < 0x800) {
            return trie_range_leaf(c, r1[c >> 6]);
        } else if (c < 0x10000) {
            auto child = r2[(c >> 6) - 0x10];
            return trie_range_leaf(c, r3.begin()[child]);
        } else {
            auto child = r4[(c >> 12) - 0x10];
            auto leaf = r5.begin()[(child << 6) + ((c >> 6) & 0b111111)];
            return trie_range_leaf(c, r6.begin()[leaf]);
        }
    }
};

struct small_bool_trie {
    std::initializer_list<std::uint8_t> r1;
    std::initializer_list<std::uint64_t> r2;

    constexpr std::size_t size() const noexcept {
        return full_size(r1) + full_size(r2);
    }

    constexpr bool operator()(char32_t u) const noexcept {
        auto c = static_cast<std::uint32_t>(u);
        auto idx = c >> 6;
        if (idx >= r1.size()) {
            return false;
        } else {
            auto child = r1.begin()[idx];
            return trie_range_leaf(c, r2.begin()[child]);
        }
    }
};

template <char32_t U>
struct single_code_point {
    constexpr std::size_t size() const noexcept {
        return 0;
    }

    constexpr bool operator()(char32_t u) const noexcept {
        return u == U;
    }
};

struct exhaustive_list16 {
    constexpr std::size_t size() const noexcept {
        return full_size(list);
    }

    constexpr bool operator()(char32_t u) const noexcept {
        if (u > 0xFFFF) {
            return false;
        }

        auto c = static_cast<std::uint16_t>(u);
        for(auto x: list) {
            if(c == x) {
                return true;
            }
        }
        return false;
    }

    std::initializer_list<std::uint16_t> list;
};

struct range_list {
    struct range {
        std::uint32_t first;
        std::uint32_t last;
    };

    constexpr std::size_t size() const noexcept {
        return full_size(list);
    }

    constexpr bool operator()(char32_t u) const noexcept {
        auto it = *std::upper_bound(list.rbegin(), list.rend(), u,
                [](char32_t u, range const& g) {
                    return u >= g.first;
                });
        return it != range.rend() && it->last >= u;
    }

    std::initializer_list<range> list;
};

struct private_use_ranges {
    constexpr std::size_t size() const noexcept {
        return 0;
    }

    constexpr bool operator()(char32_t u) const noexcept {
        return (u >= 0xE000 && u <= 0xF8FF)
            || (u >= 0xF0000 && u <= 0xFFFFD)
            || (u >= 0x100000 && u <= 0x10FFFD);
    }
};

struct noncharacter_ranges {
    constexpr std::size_t size() const noexcept {
        return 0;
    }

    constexpr bool operator()(char32_t u) const noexcept {
        return (u & 0xFFFE) == 0xFFFE;
    }
};

struct version {
    unsigned major, minor, revision;
};

}
