# Projekty
## Obecné požadavky a informace

Pošlete e-mailem, které zadání byste chtěli vypracovat, nejpozději do **9. 12. 2025**.

Termín odevzdání je **8. 2. 2026**. Odevzdejte e-mailem report a kód (odkaz na Git nebo archiv (zip/tar.*)).

Kód musí být funkční a bude obsahovat README s instrukcemi, jak program zkompilovat a spustit.
Kód může být v libovolném jazyce. Pokud bude kód v Jupyter notebooku, bude odevzdán se všemi buňkami proběhnutými.

Report bude obsahovat úvod, popis použitých metod, výsledky a závěr.
Popis použitých metod se očekává na 1–2 strany.

Report je doporučeno napsat v LaTeXu:
```
\documentclass[11pt]{article}
\usepackage{geometry}
\geometry{a4paper, includefoot, nomarginpar, left=25mm, right=25mm, top=25mm, bottom=25mm}
```
Otestujte algoritmy alespoň na 3 ruzných problémech.

Pokud budete testovat na maticích a není řečeno jinak, vyberte si matice ze [SuiteSparse Matrix Collection](https://sparse.tamu.edu).

V projektech využívajících PETSc/SLEPc můžete provádět testování i paralelně.

---

1. ## Srovnání vybraných EPS typů řešičů ve SLEPc pro největší vlastní čísla
    Cílem projektu je porovnat efektivitu vybraných metod řešení úloh na vlastní čísla pomocí knihovny SLEPc.
    Zaměřte se zejména na výpočet jednoho nebo několika největších vlastních čísel.

    ### Požadavky
    - Otestujte minimálně mocninnou metodu, Jacobi–Davidson a Krylov–Schur.
    - Porovnávejte: rychlost konvergence a výpočetní náročnost.

1. ## Srovnání SVD a randomizovaného SVD
   Porovnejte klasickou SVD s randomizovanou SVD z hlediska rychlosti, paměťové náročnosti a přesnosti aproximace pro různé typy matic.

   ### Požadavky
   - Implementace / použití SVD a randomized SVD.
   - Měření: čas výpočtu, paměť, chyba.
   - Analýza kompromisu mezi přesností a rychlostí.

1. ## Srovnání komprese dat pomocí SVD a waveletů
   Porovnejte účinnost komprese dat pomocí SVD a pomocí waveletové transformace na vybraných obrázcích nebo signálech.

   ### Požadavky
   - Implementujte kompresi pomocí SVD i waveletů.
   - Testy na obrázcích či signálech.
   - Měření: poměr komprese, kvalita rekonstrukce, čas komprese/dekomprese.
   - Analýza vlivu parametrů (počet singulárních hodnot, počet úrovní waveletovského rozkladu).

1. ## Implementace SVD pomocí Golub–Kahan bidiagonalizace pro husté matice
   Implementujte SVD založenou na Golub–Kahanově bidiagonalizaci a porovnejte ji s knihovními implementacemi na hustých maticích.

   ### Požadavky
   - Implementace bidiagonalizace a následné diagonalizace bidiagonální matice.
   - Testy na hustých maticích různých velikostí.
   - Porovnání rychlosti a přesnosti s LAPACKem (např. NumPy/SciPy SVD).

1. ## Implementace SVD pomocí Golub–Kahan–Lanczos bidiagonalizace pro řídké matice
   Implementujte Lanczosovu variantu Golub–Kahanovy bidiagonalizace pro řídké matice a porovnejte ji s existujícími sparse SVD řešiči.

   ### Požadavky
   - Implementace Lanczos-bidiagonalizace.
   - Efektivní práce s řídkými strukturami.
   - Měření konvergence, rychlosti a paměti.

1. ## Srovnání reordering algoritmů pro přímé řešiče v PETSc
   Porovnejte různé reordering algoritmy používané přímými řešiči v PETSc z hlediska času reorderingu, faktorizace, řešení a velikosti faktorů.

   ### Požadavky
   - Použijte LU z PETSc.
   - Vyzkoušejte několik algoritmů `MatOrderingType`.
   - Měření: čas reorderingu, čas faktorizace, čas řešení, paměť/fill-in.

1. ## Srovnání přímých řešičů v PETSc
   Porovnejte různé přímé řešiče dostupné v PETSc (MUMPS, PaStiX, SuperLU...) z hlediska rychlosti faktorizace a řešení.

   ### Požadavky
   - Měřte čas faktorizace a řešení.

1. ## Srovnání předpodmiňovačů pro KSPCG v PETSc
   Porovnejte efektivitu různých předpodmiňovačů pro KSPCG v PETSc.

   ### Požadavky
   - Otestujte předpodmiňovače: Jacobi, SOR, ILU/ICC a případně GAMG.
   - Měření: počet iterací a čas.

   **Srovnání předpodmiňovačů dává smysl jen tehdy, když `KSPSetNormType(ksp, KSP_NORM_UNPRECONDITIONED).`**

1. ## Srovnání předpodmiňovačů pro KSPGMRES v PETSc
   Porovnejte efektivitu různých předpodmiňovačů pro KSPGMRES v PETSc.

   ### Požadavky
   - Otestujte nepředpodmíněné GMRES a předpodmiňovače Jacobi, SOR, ILU/ICC a případně GAMG.
   - Měření: počet iterací a čas.
   - Případně otestujte různá nastavení restartu.

   **Srovnání předpodmiňovačů dává smysl jen tehdy, když `KSPSetNormType(ksp, KSP_NORM_UNPRECONDITIONED).`**

1. ## Srovnání metod pro řešení least squares problému v PETSc
   Porovnejte různé metody řešení least-squares problémů dostupné v PETSc (např. LSQR, BCGS, BICG, CGNE).

   ### Požadavky
   - Testujte na obdelníkových maticích.
   - Měření: počet iterací a čas.
   - Bez předpodmínění.

1. ## Gram–Schmidtův a modifikovaný Gram–Schmidtův proces
   Porovnejte klasický a modifikovaný Gram–Schmidtův proces z hlediska numerické stability a případně i paralelní škálovatelnosti.

   ### Požadavky
   - Implementujte CGS a MGS.
   - Měření ztráty ortogonality a numerické chyby.
   - Vyzkoušejte na maticících s řádově ruznýmí čísly podmíněnosti.

1. ## Implementace a porovnání metod největšího spádu s optimalní a Barzilai-Borwein délkami kroků a CG
   Implementujte metodu největšího spádu s optimalní a Barzilai-Borwein délkami kroků a CG. Metody porovnejte z hlediska rychlosti konvergence a času výpočtu.

   ### Požadavky
   - Implementace metody největšího spádu s optimalní a Barzilai-Borwein délkami kroků a CG.
   - Porovnání počtů iterací a časů mezi jednotlivými metodami.

1. ## Implementace vlastního předpodmíněného CG v PETSc a porovnání s KSPCG
   Implementujte vlastní předpodmíněnou verzi CG v rámci PETSc a porovnejte ji s vestavěným KSPCG.

   ### Požadavky
   - Implementace CG s podporou předpodmínění (využíjte PC objekt v PETSc)
   - Porovnání správnosti výsledků, počtu iterací a času s KSPCG.

   **Srovnání předpodmiňovačů dává smysl jen tehdy, když `KSPSetNormType(ksp, KSP_NORM_UNPRECONDITIONED).`**
   **Pozor na defaultní nastavení předpodmiňovače v PETSc.**

---

# Pokročilé projekty
U těchto projektů se očekává konzultace zadání.

1. ## Vlastní zadání

1. ## Paralelní srovnání CG a pipeline CG metod (cg, groppcg, pipecg, pipecg2, pipelcg, pipeprcg, ...)

1. ## Naimplementujte vlastní nepředpodmíněné GMRES v PETSc a srovnejte s KSPGMRES

1. ## Srovnání EPStype řešičů ve SLEPc pro nejmenší vlastní čísla

1. ## Komprese hlubokých neuronových sítí pomocí SVD

1. ## Aplikace PCA na rozpoznávání tváří (eigenface)

1. ## Aplikace SVD komprese na video

1. ## PageRank recommender system (např. pro filmy)

