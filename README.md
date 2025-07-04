# High-School Timetable Scheduler  

This repository contains **`main.cpp`**, a self-contained C++17 program that automatically builds weekly timetables for a Vietnamese high-school.  
It assigns every teaching `phancong` (teacher–class–subject–period load) to concrete periods while respecting hard constraints and minimising soft-constraint penalties.

---
## 1.  Input files
| File | Role |
|------|------|
| **`PC_HK1.txt`** / **`PC_HK2.txt`** | Semester-1 / semester-2 teaching assignments. Each line:<br>`<PC_ID> <Class> <Subject> <TeacherID> <Periods> <BlockLength>` |
| **`VP_chitiet.txt`** | (generated) Detailed violation report |

Example line from `PC_HK1.txt`  
```
PC001 10A Anh GV1024 3 2
```
means: assignment ID `PC001`, class **10A**, subject **English**, taught by **GV1024**, 3 periods per week planned as blocks of 2 consecutive periods.

Hard-coded constants in `main.cpp` allow switching semester (`int HK = 1`) and indicate available ICT rooms etc.

---
## 2.  Core data structures (see lines 1–110)
* `struct phancong`   — one teaching assignment (input).
* `struct tlop` / `struct tklop`   — one period cell and the 30-cell array for a class (10 periods × 3 days or 5 days × 6?; index 1-based).
* `struct tgv` / `struct tkgv`   — symmetric structure for each teacher.
* Global arrays track free/occupied cells (`lop_tiet`, `gv_tiet`) and per-category violation counters (`VP_lop`, `VP_gv`).

---
## 3.  Scheduling pipeline
1. **Read input** (`nhap`) and **normalise** period-block lengths (`suaCumTiet`).  
2. **Priority tagging** (`ghiMucUuTien`)  
   * SHL (homeroom) → priority 0 (must be placed first).  
   * Literature/PE → 1, Math/English → 2, others → 3.
3. **Sort assignments** (`sapXep`) by (priority, total periods taught by that teacher in that subject, block size).
4. **Build class/teacher lists** (`taoDanhSachLop`, `taoDanhSachGiaoVien`) and sort classes by "complexity" (many different teachers) (`SortDanhSachLop`).
5. **Greedy placement** – for each class (`Xeplop → Xepmotlop`) every assignment is inserted by scanning the timetable (`findslot`, `XepPhanCong`) until a feasible window is found that satisfies **hard constraints** (see below).
6. **Improvement phase 1** (`CaiThien1`)  
   – deterministic gap filling, swapping, pushing blocks upward to remove trailing empty cells.
7. **Improvement phase 2** (`CaiThien2`)  
   – random local-search / hill-climbing run (~400 k iterations) that swaps two random cells of a class and keeps the move if the overall penalty `TinhDiemViPham` decreases.
8. The improvement loop repeats up to *10* times if unplaced assignments remain.
9. **Output generation**  
   * `TKB_lop.txt` – timetable per class  
   * `TKB_gv.txt` – timetable per teacher  
   * `VP_*` – violation summaries (per class, per teacher, total).

---
## 4.  Constraint model
### 4.1 Hard constraints (H)
| ID | Function | Meaning |
|----|----------|---------|
| H1 | `kiemTraTrungGioGiaoVien` | A teacher cannot be in two classes at the same period |
| H2 | `kiemTraGioKhongXep` | Forbidden hours for certain subjects (e.g. afternoon PE) |
| H3 | `kiemTraDungDoPhongHoc` | Number of simultaneous IT lessons ≤ available computer rooms |
| H4 | – (reserved) |
| H5 | `checkTietLung` / `TietkLung` | Avoid gaps (isolated periods) within a class day |
| H6 | – |
| H7 | `kiemTraGioLienTiep` | Literature / PE blocks may not cross recess |

A schedule violating any **H** constraint is rejected during placement.

### 4.2 Soft constraints (S)
After a feasible table is built, seven softer criteria are counted (`VP_Si` functions). Each has a weight in array `vp[]` and together form the **penalty score** printed at the end.

Examples:
* `S2` – a class having the same subject in both sessions of a day (`countHocCachMon`)
* `S3` – a teacher teaching both morning and afternoon (`countBuoiDaygv`)
* `S7` – >4 different subjects in one session (`countToiDaMon`)

---
## 5.  File map – important functions
```text
main.cpp
├─ nhap()                   – parse input file
├─ sapXep()                 – assignment ordering
├─ XepPhanCong()            – place one assignment
├─ check()/findslot()       – feasibility checks
├─ CaiThien1(), CaiThien2() – improvement heuristics
├─ TinhDiemViPham()         – compute global score
└─ main()                   – orchestrates the full pipeline
```

---
## 6.  Building & running
```bash
# compile
$ g++ -std=c++17 -O2 main.cpp -o scheduler

# run (default HK = 1)
$ ./scheduler
```
Generated output files will appear in the project root. To schedule the second semester set `HK = 2` around line 32 or pass `-DHK=2` at compile time.

---
## 7.  Extending / adapting
* Update the `DSlop` array (line 30) for additional classes.
* Change room counts (`slphongtin`) or penalty weights (`vp[]`).
* Add new hard constraints by extending `check()` and integrating the condition into `findslot`.

---
## 8.  License
Provided as-is for educational use.