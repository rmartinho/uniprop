#include <range_bsearch/is.h++>
#include <booltrie/is.h++>
#include <booltrie_plus/is.h++>

#include <common/bench.h++>

#include <nonius.h++>

namespace sg16 {

MAKE_BENCHES(range_bsearch)
MAKE_BENCHES(booltrie)
MAKE_BENCHES(booltrie_plus)

}
