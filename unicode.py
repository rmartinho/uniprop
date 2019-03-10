#!/usr/bin/env python

# This script uses the following Unicode tables:
# - DerivedCoreProperties.txt
# - DerivedNormalizationProps.txt
# - EastAsianWidth.txt
# - auxiliary/GraphemeBreakProperty.txt
# - PropList.txt
# - ReadMe.txt
# - Scripts.txt
# - UnicodeData.txt
#
# Since this should not require frequent updates, we just store this
# out-of-line and check the tables.rs file into git.

import fileinput, re, os, sys, operator, math, datetime

# The directory in which this file resides.
fdir = os.path.dirname(os.path.realpath(__file__)) + "/"

preamble = '''
// NOTE: The following code was generated by "./unicode.py", do not edit directly

#include <uniprop/structs.h++>

namespace sg16 {
namespace booltrie {
'''

# Mapping taken from Table 12 from:
# http://www.unicode.org/reports/tr44/#General_Category_Values
expanded_categories = {
    'Lu': ['L'], 'Ll': ['L'], 'Lt': ['L'],
    'Lm': ['L'], 'Lo': ['L'],
    'Mn': ['M'], 'Mc': ['M'], 'Me': ['M'],
    'Nd': ['N'], 'Nl': ['N'], 'No': ['N'],
    'Pc': ['P'], 'Pd': ['P'], 'Ps': ['P'], 'Pe': ['P'],
    'Pi': ['P'], 'Pf': ['P'], 'Po': ['P'],
    'Sm': ['S'], 'Sc': ['S'], 'Sk': ['S'], 'So': ['S'],
    'Zs': ['Z'], 'Zl': ['Z'], 'Zp': ['Z'],
    'Cc': ['C'], 'Cf': ['C'], 'Cs': ['C'], 'Co': ['C'], 'Cn': ['C'],
}

script_list = [
        "Adlam", "Ahom", "Anatolian_Hieroglyphs", "Arabic", "Armenian", "Avestan", "Balinese", "Bamum", "Bassa_Vah", "Batak",
        "Bengali", "Bhaiksuki", "Bopomofo", "Brahmi", "Braille", "Buginese", "Buhid", "Canadian_Aboriginal", "Carian", "Caucasian_Albanian",
        "Chakma", "Cham", "Cherokee", "Common", "Coptic", "Cuneiform", "Cypriot", "Cyrillic", "Deseret", "Devanagari",
        "Dogra", "Duployan", "Egyptian_Hieroglyphs", "Elbasan", "Elymaic", "Ethiopic", "Georgian", "Glagolitic", "Gothic", "Grantha",
        "Greek", "Gujarati", "Gunjala_Gondi", "Gurmukhi", "Han", "Hangul", "Hanifi_Rohingya", "Hanunoo", "Hatran", "Hebrew",
        "Hiragana", "Imperial_Aramaic", "Inherited", "Inscriptional_Pahlavi", "Inscriptional_Parthian", "Javanese", "Kaithi", "Kannada", "Katakana", "Kayah_Li",
        "Kharoshthi", "Khmer", "Khojki", "Khudawadi", "Lao", "Latin", "Lepcha", "Limbu", "Linear_A", "Linear_B",
        "Lisu", "Lycian", "Lydian", "Mahajani", "Makasar", "Malayalam", "Mandaic", "Manichaean", "Marchen", "Masaram_Gondi",
        "Medefaidrin", "Meetei_Mayek", "Mende_Kikakui", "Meroitic_Cursive", "Meroitic_Hieroglyphs", "Miao", "Modi", "Mongolian", "Mro", "Multani",
        "Myanmar", "Nabataean", "Nandinagari", "Newa", "New_Tai_Lue", "Nko", "Nushu", "Nyiakeng_Puachue_Hmong", "Ogham", "Ol_Chiki",
        "Old_Hungarian", "Old_Italic", "Old_North_Arabian", "Old_Permic", "Old_Persian", "Old_Sogdian", "Old_South_Arabian", "Old_Turkic", "Oriya", "Osage",
        "Osmanya", "Pahawh_Hmong", "Palmyrene", "Pau_Cin_Hau", "Phags_Pa", "Phoenician", "Psalter_Pahlavi", "Rejang", "Runic", "Samaritan",
        "Saurashtra", "Sharada", "Shavian", "Siddham", "SignWriting", "Sinhala", "Sogdian", "Sora_Sompeng", "Soyombo", "Sundanese",
        "Syloti_Nagri", "Syriac", "Tagalog", "Tagbanwa", "Tai_Le", "Tai_Tham", "Tai_Viet", "Takri", "Tamil", "Tangut",
        "Telugu", "Thaana", "Thai", "Tibetan", "Tifinagh", "Tirhuta", "Ugaritic", "Vai", "Wancho", "Warang_Citi",
        "Yi", "Zanabazar_Square"]

script_extension_list = [
        "Adlm", "Arab", "Armn", "Beng", "Bopo", "Bugi", "Buhd", "Cakm", "Copt", "Cprt",
        "Cyrl", "Deva", "Dogr", "Dupl", "Geor", "Glag", "Gong", "Gonm", "Gran", "Grek",
        "Gujr", "Guru", "Hang", "Hani", "Hano", "Hira", "Java", "Kali", "Kana", "Khoj",
        "Knda", "Kthi", "Latn", "Limb", "Lina", "Linb", "Mahj", "Mand", "Mani", "Mlym",
        "Modi", "Mong", "Mult", "Mymr", "Nand", "Orya", "Perm", "Phag", "Phlp", "Rohg",
        "Shrd", "Sind", "Sinh", "Sogd", "Sylo", "Syrc", "Tagb", "Takr", "Tale", "Taml",
        "Telu", "Tglg", "Thaa", "Tirh", "Yiii"]

# these are the surrogate codepoints, which are not valid rust characters
surrogate_codepoints = (0xd800, 0xdfff)

def fetch(f):
    path = fdir + os.path.basename(f)
    if not os.path.exists(path):
        os.system("curl -o {0}{1} ftp://ftp.unicode.org/Public/UNIDATA/{1}".format(fdir, f))

    if not os.path.exists(path):
        sys.stderr.write("cannot load %s" % f)
        exit(1)

def is_surrogate(n):
    return surrogate_codepoints[0] <= n <= surrogate_codepoints[1]

def load_unicode_data(f):
    fetch(f)
    gencats = {}
    to_lower = {}
    to_upper = {}
    to_title = {}
    combines = {}
    canon_decomp = {}
    compat_decomp = {}

    udict = {}
    range_start = -1
    for line in fileinput.input(fdir + f):
        data = line.split(';')
        if len(data) != 15:
            continue
        cp = int(data[0], 16)
        if is_surrogate(cp):
            continue
        if range_start >= 0:
            for i in range(range_start, cp):
                udict[i] = data
            range_start = -1
        if data[1].endswith(", First>"):
            range_start = cp
            continue
        udict[cp] = data

    for code in udict:
        (code_org, name, gencat, combine, bidi,
         decomp, deci, digit, num, mirror,
         old, iso, upcase, lowcase, titlecase) = udict[code]

        # generate char to char direct common and simple conversions
        # uppercase to lowercase
        if lowcase != "" and code_org != lowcase:
            to_lower[code] = (int(lowcase, 16), 0, 0)

        # lowercase to uppercase
        if upcase != "" and code_org != upcase:
            to_upper[code] = (int(upcase, 16), 0, 0)

        # title case
        if titlecase.strip() != "" and code_org != titlecase:
            to_title[code] = (int(titlecase, 16), 0, 0)

        # store decomposition, if given
        if decomp != "":
            if decomp.startswith('<'):
                seq = []
                for i in decomp.split()[1:]:
                    seq.append(int(i, 16))
                compat_decomp[code] = seq
            else:
                seq = []
                for i in decomp.split():
                    seq.append(int(i, 16))
                canon_decomp[code] = seq

        # place letter in categories as appropriate
        for cat in [gencat, "Assigned"] + expanded_categories.get(gencat, []):
            if cat not in gencats:
                gencats[cat] = []
            gencats[cat].append(code)

        # record combining class, if any
        if combine != "0":
            if combine not in combines:
                combines[combine] = []
            combines[combine].append(code)

    # generate Not_Assigned from Assigned
    gencats["Cn"] = gen_unassigned(gencats["Assigned"])
    # Other contains Not_Assigned
    gencats["C"].extend(gencats["Cn"])
    gencats = group_cats(gencats)
    combines = to_combines(group_cats(combines))

    return (canon_decomp, compat_decomp, gencats, combines, to_upper, to_lower, to_title)

def load_special_casing(f, to_upper, to_lower, to_title):
    fetch(f)
    for line in fileinput.input(fdir + f):
        data = line.split('#')[0].split(';')
        if len(data) == 5:
            code, lower, title, upper, _comment = data
        elif len(data) == 6:
            code, lower, title, upper, condition, _comment = data
            if condition.strip():  # Only keep unconditional mappins
                continue
        else:
            continue
        code = code.strip()
        lower = lower.strip()
        title = title.strip()
        upper = upper.strip()
        key = int(code, 16)
        for (map_, values) in [(to_lower, lower), (to_upper, upper), (to_title, title)]:
            if values != code:
                values = [int(i, 16) for i in values.split()]
                for _ in range(len(values), 3):
                    values.append(0)
                assert len(values) == 3
                map_[key] = values

def group_cats(cats):
    cats_out = {}
    for cat in cats:
        cats_out[cat] = group_cat(cats[cat])
    return cats_out

def group_cat(cat):
    cat_out = []
    letters = sorted(set(cat))
    cur_start = letters.pop(0)
    cur_end = cur_start
    for letter in letters:
        assert letter > cur_end, \
            "cur_end: %s, letter: %s" % (hex(cur_end), hex(letter))
        if letter == cur_end + 1:
            cur_end = letter
        else:
            cat_out.append((cur_start, cur_end))
            cur_start = cur_end = letter
    cat_out.append((cur_start, cur_end))
    return cat_out

def ungroup_cat(cat):
    cat_out = []
    for (lo, hi) in cat:
        while lo <= hi:
            cat_out.append(lo)
            lo += 1
    return cat_out

def gen_zzzz(assigned):
    ranges = [rng for (k, ranges) in assigned.iteritems() for rng in ranges]
    ranges.sort()
    zzzz = []
    last_zzzz = 0
    for rng in ranges:
        if rng[0] > last_zzzz:
            zzzz += [(last_zzzz, rng[1]-1)]
        last_zzzz = rng[1]+1
    return zzzz

def gen_unassigned(assigned):
    assigned = set(assigned)
    return ([i for i in range(0, 0xd800) if i not in assigned] +
            [i for i in range(0xe000, 0x110000) if i not in assigned])

def to_combines(combs):
    combs_out = []
    for comb in combs:
        for (lo, hi) in combs[comb]:
            combs_out.append((lo, hi, comb))
    combs_out.sort(key=lambda comb: comb[0])
    return combs_out

def format_table_content(f, content, indent):
    line = " "*indent
    first = True
    for chunk in content.split(","):
        if len(line) + len(chunk) < 98:
            if first:
                line += chunk
            else:
                line += ", " + chunk
            first = False
        else:
            f.write(line + ",\n")
            line = " "*indent + chunk
    f.write(line)

def load_properties(f, interestingprops):
    fetch(f)
    props = {}
    re1 = re.compile("^ *([0-9A-F]+) *; *(\w+)")
    re2 = re.compile("^ *([0-9A-F]+)\.\.([0-9A-F]+) *; *(\w+)")

    for line in fileinput.input(fdir + os.path.basename(f)):
        prop = None
        d_lo = 0
        d_hi = 0
        m = re1.match(line)
        if m:
            d_lo = m.group(1)
            d_hi = m.group(1)
            prop = m.group(2)
        else:
            m = re2.match(line)
            if m:
                d_lo = m.group(1)
                d_hi = m.group(2)
                prop = m.group(3)
            else:
                continue
        if interestingprops and prop not in interestingprops:
            continue
        d_lo = int(d_lo, 16)
        d_hi = int(d_hi, 16)
        if prop not in props:
            props[prop] = []
        props[prop].append((d_lo, d_hi))

    # optimize if possible
    for prop in props:
        props[prop] = group_cat(ungroup_cat(props[prop]))

    return props

def load_script_extensions(f, interestingprops):
    fetch(f)
    props = {}
    re1 = re.compile("^ *([0-9A-F]+) *; *(( |\w)+) #")
    re2 = re.compile("^ *([0-9A-F]+)\.\.([0-9A-F]+) *; *(( |\w)+) #")

    for line in fileinput.input(fdir + os.path.basename(f)):
        prop = None
        d_lo = 0
        d_hi = 0
        m = re1.match(line)
        if m:
            d_lo = m.group(1)
            d_hi = m.group(1)
            propl = m.group(2)
        else:
            m = re2.match(line)
            if m:
                d_lo = m.group(1)
                d_hi = m.group(2)
                propl = m.group(3)
            else:
                continue

        d_lo = int(d_lo, 16)
        d_hi = int(d_hi, 16)
        for prop in propl.split(' '):
            if interestingprops and prop not in interestingprops:
                continue
            if prop not in props:
                props[prop] = []
            props[prop].append((d_lo, d_hi))

    # optimize if possible
    for prop in props:
        props[prop] = group_cat(ungroup_cat(props[prop]))

    return props

def escape_char(c):
    return "'\\u{%x}'" % c if c != 0 else "'\\0'"

def emit_table(f, name, t_data, t_type = "&[(char, char)]", is_pub=True,
        pfun=lambda x: "(%s,%s)" % (escape_char(x[0]), escape_char(x[1]))):
    f.write("constexpr %s %s = &{\n" % (t_type, name))
    data = ""
    first = True
    for dat in t_data:
        if not first:
            data += ","
        first = False
        data += pfun(dat)
    format_table_content(f, data, 4)
    f.write("\n    };\n\n")

def compute_trie(rawdata, chunksize):
    root = []
    childmap = {}
    child_data = []
    for i in range(len(rawdata) // chunksize):
        data = rawdata[i * chunksize: (i + 1) * chunksize]
        child = '|'.join(map(str, data))
        if child not in childmap:
            childmap[child] = len(childmap)
            child_data.extend(data)
        root.append(childmap[child])
    return (root, child_data)

def emit_bool_trie(f, name, t_data, is_pub=True):
    CHUNK = 64
    rawdata = [False] * 0x110000
    for (lo, hi) in t_data:
        for cp in range(lo, hi + 1):
            rawdata[cp] = True

    # convert to bitmap chunks of 64 bits each
    chunks = []
    for i in range(0x110000 // CHUNK):
        chunk = 0
        for j in range(64):
            if rawdata[i * 64 + j]:
                chunk |= 1 << j
        chunks.append(chunk)

    f.write("constexpr bool_trie %s = {\n" % name)
    f.write("    {\n")
    data = ','.join('0x%016x' % chunk for chunk in chunks[0:0x800 // CHUNK])
    format_table_content(f, data, 8)
    f.write("\n    },\n")

    # 0x800..0x10000 trie
    (r2, r3) = compute_trie(chunks[0x800 // CHUNK : 0x10000 // CHUNK], 64 // CHUNK)
    f.write("    {\n")
    data = ','.join(str(node) for node in r2)
    format_table_content(f, data, 8)
    f.write("\n    },\n")
    f.write("    {\n")
    data = ','.join('0x%016x' % chunk for chunk in r3)
    format_table_content(f, data, 8)
    f.write("\n    },\n")

    # 0x10000..0x110000 trie
    (mid, r6) = compute_trie(chunks[0x10000 // CHUNK : 0x110000 // CHUNK], 64 // CHUNK)
    (r4, r5) = compute_trie(mid, 64)
    f.write("    {\n")
    data = ','.join(str(node) for node in r4)
    format_table_content(f, data, 8)
    f.write("\n    },\n")
    f.write("    {\n")
    data = ','.join(str(node) for node in r5)
    format_table_content(f, data, 8)
    f.write("\n    },\n")
    f.write("    {\n")
    data = ','.join('0x%016x' % chunk for chunk in r6)
    format_table_content(f, data, 8)
    f.write("\n    },\n")

    f.write("};\n\n")

def emit_small_bool_trie(f, name, t_data, is_pub=True):
    last_chunk = max(hi // 64 for (lo, hi) in t_data)
    n_chunks = last_chunk + 1
    chunks = [0] * n_chunks
    for (lo, hi) in t_data:
        for cp in range(lo, hi + 1):
            if cp // 64 >= len(chunks):
                print(cp, cp // 64, len(chunks), lo, hi)
            chunks[cp // 64] |= 1 << (cp & 63)

    f.write("constexpr small_bool_trie %s = {\n"
            % name)

    (r1, r2) = compute_trie(chunks, 1)

    f.write("    {\n")
    data = ','.join(str(node) for node in r1)
    format_table_content(f, data, 8)
    f.write("\n    },\n")

    f.write("    {\n")
    data = ','.join('0x%016x' % node for node in r2)
    format_table_content(f, data, 8)
    f.write("\n    },\n")

    f.write("};\n\n")

def emit_exhaustive_list16(f, name, t_data, is_pub=True):
    f.write("constexpr exhaustive_list16 %s = {\n"
            % name)

    f.write("    {\n")
    data = ','.join(('0x%04x' % u) for subrange in (range(pair[0], pair[1]+1) for pair in t_data) for u in subrange)
    format_table_content(f, data, 8)
    f.write("\n    },\n")

    f.write("};\n\n")

def emit_range_list(f, name, t_data, is_pub=True):
    f.write("constexpr range_list %s = {\n"
            % name)

    f.write("    {\n")
    data = ','.join(('{ 0x%08x, 0x%08x }' % pair) for pair in t_data)
    format_table_content(f, data, 8)
    f.write("\n    },\n")

    f.write("};\n\n")

def emit_private_use_ranges(f, name, t_data, is_pub=True):
    f.write("constexpr private_use_ranges %s = {};\n\n"
            % name)

def emit_noncharacter_ranges(f, name, t_data, is_pub=True):
    f.write("constexpr noncharacter_ranges %s = {};\n\n"
            % name)

def emit_single_code_point(f, name, t_data, is_pub=True):
    code_point = "U'\\U%08x'" % t_data[0][0]

    f.write("constexpr single_code_point<%s> %s = {\n"
            % (code_point, name))

    f.write("    {\n")
    data = ','.join(('0x%04x' % u) for subrange in (range(pair[0], pair[1]+1) for pair in t_data) for u in subrange)
    format_table_content(f, data, 8)
    f.write("\n    },\n")

    f.write("};\n\n")

def emit_property_module(f, mod, tbl, emit):
    f.write("namespace %s {\n\n" % mod)

    for cat in sorted(emit):
        if cat in ["Cc", "White_Space"]:
            emit_small_bool_trie(f, "%s_table" % cat, tbl[cat])
        elif cat in ["Lt", "Me", "Pc", "Pd", "Pf", "Pi", "Z", "Zs"]:
            emit_exhaustive_list16(f, "%s_table" % cat, tbl[cat])
        elif cat in ["Co"]:
            emit_private_use_ranges(f, "%s_table" % cat, tbl[cat])
        elif cat in ["Cn", "Noncharacter_Code_Point"]:
            emit_noncharacter_ranges(f, "%s_table" % cat, tbl[cat])
        elif cat in ["Zl", "Zp"]:
            emit_single_code_point(f, "%s_table" % cat, tbl[cat])
        elif cat in script_list:
            emit_range_list(f, "%s_table" % cat, tbl[cat])
        elif cat in ["Hani"]:
            emit_range_list(f, "%s_table" % cat, tbl[cat])
        elif cat in script_extension_list:
            emit_exhaustive_list16(f, "%s_table" % cat, tbl[cat])
        else:
            emit_bool_trie(f, "%s_table" % cat, tbl[cat])

    f.write("}\n")


def emit_conversions_module(f, to_upper, to_lower, to_title):
    f.write("pub mod conversions {")
    f.write("""
    pub fn to_lower(c: char) -> [char; 3] {
        match bsearch_case_table(c, to_lowercase_table) {
            None        => [c, '\\0', '\\0'],
            Some(index) => to_lowercase_table[index].1,
        }
    }

    pub fn to_upper(c: char) -> [char; 3] {
        match bsearch_case_table(c, to_uppercase_table) {
            None        => [c, '\\0', '\\0'],
            Some(index) => to_uppercase_table[index].1,
        }
    }

    fn bsearch_case_table(c: char, table: &[(char, [char; 3])]) -> Option<usize> {
        table.binary_search_by(|&(key, _)| key.cmp(&c)).ok()
    }

""")
    t_type = "&[(char, [char; 3])]"
    pfun = lambda x: "(%s,[%s,%s,%s])" % (
        escape_char(x[0]), escape_char(x[1][0]), escape_char(x[1][1]), escape_char(x[1][2]))
    emit_table(f, "to_lowercase_table",
        sorted(to_lower.items(), key=operator.itemgetter(0)),
        is_pub=False, t_type = t_type, pfun=pfun)
    emit_table(f, "to_uppercase_table",
        sorted(to_upper.items(), key=operator.itemgetter(0)),
        is_pub=False, t_type = t_type, pfun=pfun)
    f.write("}\n\n")

def emit_norm_module(f, canon, compat, combine, norm_props):
    canon_keys = sorted(canon.keys())

    compat_keys = sorted(compat.keys())

    canon_comp = {}
    comp_exclusions = norm_props["Full_Composition_Exclusion"]
    for char in canon_keys:
        if any(lo <= char <= hi for lo, hi in comp_exclusions):
            continue
        decomp = canon[char]
        if len(decomp) == 2:
            if decomp[0] not in canon_comp:
                canon_comp[decomp[0]] = []
            canon_comp[decomp[0]].append( (decomp[1], char) )
    canon_comp_keys = sorted(canon_comp.keys())

if __name__ == "__main__":
    r = fdir + "tables.cpp"
    if os.path.exists(r):
        os.remove(r)
    with open(r, "w") as rf:
        # write the file's preamble
        rf.write(preamble)

        # download and parse all the data
        fetch("ReadMe.txt")
        with open(fdir + "ReadMe.txt") as readme:
            pattern = "for Version (\d+)\.(\d+)\.(\d+) of the Unicode"
            unicode_version = re.search(pattern, readme.read()).groups()
        rf.write("""
constexpr version unicode_version = { %s, %s, %s };

""" % unicode_version)
        (canon_decomp, compat_decomp, gencats, combines,
                to_upper, to_lower, to_title) = load_unicode_data("UnicodeData.txt")
        load_special_casing("SpecialCasing.txt", to_upper, to_lower, to_title)
        want_derived = ["Alphabetic", "Lowercase", "Uppercase", "Default_Ignorable_Code_Point"]
        derived = load_properties("DerivedCoreProperties.txt", want_derived)
        scripts = load_properties("Scripts.txt", script_list)
        # generate Zzzz from Script
        scripts["Unknown"] = gen_zzzz(scripts)
        script_exts = load_script_extensions("ScriptExtensions.txt", script_extension_list)
        props = load_properties("PropList.txt", ["White_Space", "Noncharacter_Code_Point"])
        norm_props = load_properties("DerivedNormalizationProps.txt", ["Full_Composition_Exclusion"])

        # category tables
        for (name, cat, pfuns) in ("general_category", gencats,
                                    ["C", "Cc", "Cf", "Cn", "Co",
                                    "L", "Ll", "Lm", "Lo", "Lt", "Lu",
                                    "M", "Mc", "Me", "Mn",
                                    "N", "Nd", "Nl", "No",
                                    "P", "Pc", "Pd", "Pe", "Pf", "Pi", "Po", "Ps",
                                    "S", "Sc", "Sk", "Sm", "So",
                                    "Z", "Zl", "Zp", "Zs"]), \
                                  ("derived_property", derived, want_derived), \
                                  ("property", props, ["White_Space"]), \
                                  ("script", scripts, script_list + ["Unknown"]), \
                                  ("script_ext", script_exts, script_extension_list):
            emit_property_module(rf, name, cat, pfuns)

        # normalizations and conversions module
        #emit_norm_module(rf, canon_decomp, compat_decomp, combines, norm_props)
        #emit_conversions_module(rf, to_upper, to_lower, to_title)
        rf.write("}\n}")
    print("Regenerated tables.cpp.")

