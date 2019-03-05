#pragma once

#include <common/general_category.h++>

#include <iterator>
#include <algorithm>
#include <cstddef>

namespace sg16 {
namespace range_bsearch {

struct general_category_range {
    char32_t start;
    general_category value;
};

extern general_category_range const* general_category_data;
extern std::size_t general_category_data_size;

template <general_category Cat>
bool is(char32_t u) noexcept {
    auto begin = std::make_reverse_iterator(general_category_data + general_category_data_size);
    auto end = std::make_reverse_iterator(general_category_data);
    auto range = *std::upper_bound(begin, end, u,
            [](char32_t u, general_category_range const& g) {
                return u >= g.start;
            });
    return range.value == Cat;
}

inline const bool total_size = general_category_data_size * sizeof(general_category_range);

template <general_category Cat>
inline const bool size_for = total_size;

}
}
