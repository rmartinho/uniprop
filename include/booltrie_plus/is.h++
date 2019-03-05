#pragma once

#include <common/general_category.h++>
#include <common/structs.h++>
#include <booltrie/is.h++>

namespace sg16 {
namespace booltrie_plus {

template <general_category Cat>
constexpr auto table_for = sg16::booltrie::table_for<Cat>;

template <>
constexpr small_bool_trie table_for<general_category::cc> = {
    {
        0, 1, 0
    },
    {
        0x00000000ffffffff, 0x8000000000000000
    },
};

template <>
constexpr private_use_ranges table_for<general_category::co> = {};

template <>
constexpr exhaustive_list16 table_for<general_category::lt> = {
    {
         0x1C5,  0x1C8,  0x1CB,  0x1F2,
        0x1F88, 0x1F89, 0x1F8A, 0x1F8B,
        0x1F8C, 0x1F8D, 0x1F8E, 0x1F8F,
        0x1F98, 0x1F99, 0x1F9A, 0x1F9B,

        0x1F9C, 0x1F9D, 0x1F9E, 0x1F9F,
        0x1FA8, 0x1FA9, 0x1FAA, 0x1FAB,
        0x1FAC, 0x1FAD, 0x1FAE, 0x1FAF,
        0x1FBC, 0x1FCC,
    }
};

template <>
constexpr exhaustive_list16 table_for<general_category::me> = {
    {
         0x488,  0x489, 0x1ABE, 0x20DD,
        0x20DE, 0x20DF, 0x20E0, 0x20E2,
        0x20E3, 0x20E4, 0xA670,
    }
};

template <>
constexpr exhaustive_list16 table_for<general_category::pc> = {
    {
          0x5F, 0x203F, 0x2040, 0x2054,
        0xFE33, 0xFE34, 0xFE4D, 0xFE4E,
        0xFE4F, 0xFF3F,
    }
};

template <>
constexpr exhaustive_list16 table_for<general_category::pd> = {
    {
          0x2D,  0x58A,  0x5BE, 0x1400,
        0x1806, 0x2010, 0x2011, 0x2012,
        0x2013, 0x2014, 0x2015, 0x2E17,
        0x2E1A, 0x2E3A, 0x2E3B, 0x2E40,

        0x301C, 0x3030, 0x30A0, 0xFE31,
        0xFE32, 0xFE58, 0xFE63, 0xFF0D,
    }
};

template <>
constexpr exhaustive_list16 table_for<general_category::pf> = {
    {
          0xBB, 0x2019, 0x201D, 0x203A,
        0x2E03, 0x2E05, 0x2E0A, 0x2E0D,
        0x2E1D, 0x2E21,
    }
};

template <>
constexpr exhaustive_list16 table_for<general_category::pi> = {
    {
          0xAB, 0x2018, 0x201B, 0x201F,
        0x2039, 0x2E02, 0x2E04, 0x2E09,
        0x2E0C, 0x2E1C, 0x2E20,
    }
};

template <>
constexpr exhaustive_list16 table_for<general_category::z> = {
    {
          0x20,   0xA0, 0x1680, 0x2000,
        0x2001, 0x2002, 0x2003, 0x2004,
        0x2005, 0x2006, 0x2007, 0x2008,
        0x2009, 0x200A, 0x2028, 0x2029,

        0x202F, 0x205F, 0x3000,
    }
};

template <>
constexpr single_code_point<U'\u2028'> table_for<general_category::zl> = {};

template <>
constexpr single_code_point<U'\u2029'> table_for<general_category::zp> = {};

template <>
constexpr exhaustive_list16 table_for<general_category::zs> = {
    {
          0x20,   0xA0, 0x1680, 0x2000,
        0x2001, 0x2002, 0x2003, 0x2004,
        0x2005, 0x2006, 0x2007, 0x2008,
        0x2009, 0x200A, 0x202F, 0x205F,

        0x3000,
    }
};

template <general_category Cat>
bool is(char32_t u) noexcept {
    return table_for<Cat>(u);
}

inline const bool total_size =
    table_for<general_category::c>.size() +
    table_for<general_category::cc>.size() +
    table_for<general_category::cf>.size() +
    table_for<general_category::cn>.size() +
    table_for<general_category::co>.size() +
    // table_for<general_category::cs>.size() +
    table_for<general_category::l>.size()  +
    table_for<general_category::ll>.size() +
    table_for<general_category::lm>.size() +
    table_for<general_category::lo>.size() +
    table_for<general_category::lt>.size() +
    table_for<general_category::lu>.size() +
    table_for<general_category::m>.size()  +
    table_for<general_category::mc>.size() +
    table_for<general_category::me>.size() +
    table_for<general_category::mn>.size() +
    table_for<general_category::n>.size() +
    table_for<general_category::nd>.size() +
    table_for<general_category::nl>.size() +
    table_for<general_category::no>.size() +
    table_for<general_category::p>.size()  +
    table_for<general_category::pc>.size() +
    table_for<general_category::pd>.size() +
    table_for<general_category::pe>.size() +
    table_for<general_category::pf>.size() +
    table_for<general_category::pi>.size() +
    table_for<general_category::po>.size() +
    table_for<general_category::ps>.size() +
    table_for<general_category::sc>.size() +
    table_for<general_category::sk>.size() +
    table_for<general_category::sm>.size() +
    table_for<general_category::so>.size() +
    table_for<general_category::z>.size()  +
    table_for<general_category::zl>.size() +
    table_for<general_category::zp>.size() +
    table_for<general_category::zs>.size();

template <general_category Cat>
inline const bool size_for = table_for<Cat>.size();

}
}
