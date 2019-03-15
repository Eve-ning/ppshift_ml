### PPSHIFT
ppshift is meant to be an overhaul on how analysts look at map difficulty, where I take a detour towards machine learning instead of pure algorithms

## Is it good

No, it's not good enough for production, however, feel free to reference this as learning from mistakes

## Research Steps in a nutshell

- Get replays & beatmaps
- Match the replays to beatmaps
- Parse Beatmaps, deconstructing them into small parameters
- Teach the machine that the pattern at a certain offset results in player X performing well/badly

## Issues

The issues are described in the PDF link under this, but I'll write them here too.

### The model isn't reliable

While I think the model is good to a certain degree, I don't think it's stable enough compared to a non-black box model. In other words, I don't think this model is production ready for a few reasons:


- The model doesn't calculate less popular key counts well
- The model leans to the Top 50 population, so
  - The model is bad at calculating easy maps as there's little to no data with regards to deviation in those
  - The model is bad at matching situations where 2 maps are actually the same difficulty, but due to low interaction, the medians are vastly different.
  - The model doesn't have enough results for bad deviation situations.
  - The model seems to be reliably calculating how hard is it to get a very high score (i.e. Varying LN ends are hard to perfect, compared to hard jacks), however, most player's perception of difficulty rating doesn't fall in line with that.
- The model has very strong bias towards maps that are popular, e.g. Triumph \& Regret, which seems to be heavily affected by this issue
- Even if the model works, it's hard to explain what happens in the model since the neural network acts like a black-box.

### How to fine-tune the model

I think the main reason of this issue is the \textbf{Assumption of the Top 50}. In other words, we assumed that the Top 50 results' median can be treated like a player. However, this assumption proved to be very disastrous in terms of reliability.

- One way to prevent this is to look at specific player's replays and do the same modelling again, however, we will pivot from the player's perspective.
- We could have also, instead of looking at Top 50, we would focus on the a specific range of scores (which is painfully annoying to grab from the API), e.g. $ 750000 - 850000$, in which will give us more information on bad deviations instead of  extremely high scores with less bad deviations.
- We could have dropped the idea of looking at key counts over 7 due to the small amount of data we would have gotten from them. This has created a lot of noise in the model. 
- We did not take into account in-depth reading difficulty (i.e. how hard is it to read a broken stair compared to a smooth one). If we could've calculated that one reliably, it would've smoothed out the LN map difficulties
- If we were able to grab Double Time results, it'll double our data, and increased the pool of harder maps, this makes it significantly easier for the machine to rate them.


#### [Research Steps (For my own reference)](https://github.com/Eve-ning/ppshift_ml/blob/master/research_tex/main.pdf)

# Results and Plots

These are the results.
Lower the score, the better.
The score is the mean of deviation between the original and actual graph
p(X) is the percentile

| Score | Metadata                                                                                                            | p15  | p25  | p50   | p75   | p85   |
|-------|---------------------------------------------------------------------------------------------------------------------|------|------|-------|-------|-------|
| 1.15  | typeMARS - Triumph &amp; Regret (Regret) &lt;[ A v a l o n ]&gt;                                                    | 6.28 | 6.41 | 6.70  | 7.29  | 8.00  |
| 1.80  | ginkiha - Anemoi (Daybreak) &lt;[ A v a l o n ]&gt;                                                                 | 6.28 | 6.42 | 6.75  | 7.35  | 7.64  |
| 1.43  | ginkiha - Borealis (GRAVITY) &lt;[ A v a l o n ]&gt;                                                                | 6.26 | 6.44 | 6.85  | 7.50  | 7.91  |
| 1.22  | xi - over the top (Extra) &lt;Zan -&gt;                                                                             | 6.68 | 6.80 | 7.04  | 7.55  | 7.84  |
| 0.97  | Hermit - Dysnomia (Tidek's 4K Monochrome) &lt;-Kamikaze-&gt;                                                        | 6.53 | 6.69 | 7.04  | 7.76  | 8.08  |
| 1.00  | Imperial Circus Dead Decadence - Uta (Tragic Ends) &lt;pkk&gt;                                                      | 6.52 | 6.71 | 7.05  | 7.55  | 7.85  |
| 2.15  | Utsu-P feat.Kagamine Rin - Tokyo Teddy Bear (SHD) &lt;puxtu&gt;                                                     | 6.53 | 6.72 | 7.19  | 7.92  | 8.38  |
| 1.43  | Team Grimoire - G1ll35 d3 R415 (Shana's Extra) &lt;Allezard&gt;                                                     | 6.80 | 6.99 | 7.47  | 8.12  | 8.54  |
| 1.19  | MAZARE - Mazare Party (Ash's 4K Extra) &lt;Insp1r3&gt;                                                              | 6.95 | 7.14 | 7.52  | 8.11  | 8.42  |
| 1.54  | Team Grimoire - G1ll35 d3 R415 (L45T C4LL) &lt;Allezard&gt;                                                         | 6.89 | 7.13 | 7.55  | 8.24  | 8.85  |
| 0.87  | Colorful Sounds Port - ETERNAL DRAIN (Black Another) &lt;Wh1teh&gt;                                                 | 6.90 | 7.09 | 7.55  | 7.96  | 8.09  |
| 1.18  | TeamGrimoire+amaneko - croiX (GRAVITY) &lt;Takane6&gt;                                                              | 6.80 | 6.98 | 7.63  | 8.35  | 8.94  |
| 1.44  | Helblinde - Memoria (Original Mix) (Memories) &lt;Manwon&gt;                                                        | 6.54 | 6.82 | 7.64  | 8.25  | 8.55  |
| 1.20  | Hypernite Industries - Speedcore 300 (Extra) &lt;nowsmart&gt;                                                       | 6.93 | 7.16 | 7.64  | 8.49  | 8.94  |
| 1.03  | kamome sano Electric Orchestra - HE4VEN ~Tengoku e Youkoso~ (HEAVENLY) &lt;Fresh Chicken&gt;                        | 6.84 | 7.06 | 7.71  | 8.61  | 9.23  |
| 1.10  | ZOGRAPHOS (Yu_Asahina+Yamajet) - Verse IV (INFINITE) &lt;Ichigaki&gt;                                               | 6.83 | 7.11 | 7.77  | 8.46  | 8.98  |
| 1.45  | Team Grimoire - C18H27NO3(extend) (4K Capsaicin) &lt;[Shana Lesus]&gt;                                              | 6.66 | 7.01 | 7.78  | 8.37  | 8.72  |
| 0.75  | Kobaryo - Dotabata Animation [feat. t+pazolite] (Ultra) &lt;YaHao&gt;                                               | 6.83 | 7.24 | 7.86  | 8.56  | 8.92  |
| 0.99  | Camellia as "Bang Riot" - Blastix Riotz (Jinjin's INFINITE) &lt;Fresh Chicken&gt;                                   | 7.15 | 7.46 | 7.88  | 8.65  | 9.14  |
| 1.29  | Kurokotei - Galaxy Collapse (Cataclysmic Hypernova) &lt;Mat&gt;                                                     | 6.91 | 7.36 | 7.98  | 8.77  | 9.35  |
| 1.28  | Team Grimoire - Sheriruth (Arzenvald's EXtinction) &lt;DoNotMess&gt;                                                | 6.97 | 7.32 | 8.02  | 8.68  | 9.19  |
| 0.64  | Colorful Sounds Port - ETERNAL DRAIN (Eternal) &lt;Wh1teh&gt;                                                       | 6.97 | 7.37 | 8.02  | 9.21  | 9.82  |
| 0.67  | UNDEAD CORPORATION - The Empress scream off ver (Zenx's SHD) &lt;TheZiemniax&gt;                                    | 7.16 | 7.35 | 8.07  | 8.73  | 9.00  |
| 1.02  | Chroma - I (Chicken AI's Maximum) &lt;Lude&gt;                                                                      | 7.21 | 7.56 | 8.08  | 8.89  | 9.58  |
| 1.60  | Kaneko Chiharu - Zettai Reido (GRAVITY) &lt;SpectorDG&gt;                                                           | 7.21 | 7.52 | 8.10  | 8.87  | 9.38  |
| 2.57  | S-C-U feat. Qrispy Joybox - anemone (Kawa &amp; Julie's 7K Extra) &lt;Julie&gt;                                     | 7.52 | 7.74 | 8.10  | 8.46  | 8.77  |
| 0.98  | RoughSketch feat.Aikapin - Grimm (Kobaryo's FTN-Remix) (Grimmpossible) &lt;CHARGE&gt;                               | 6.83 | 7.37 | 8.12  | 8.93  | 9.58  |
| 1.10  | AAAA - Hoshi o Kakeru Adventure ~ we are forever friends! ~ [Long ver.] (Epochal Adventure) &lt;Lude&gt;            | 7.24 | 7.57 | 8.23  | 9.01  | 9.43  |
| 1.12  | Camellia as "Bang Riot" - Blastix Riotz (Shirou's EXTRA) &lt;Fresh Chicken&gt;                                      | 7.09 | 7.49 | 8.26  | 9.18  | 9.99  |
| 2.51  | Seiryu - Time to Air (Bruce's 7K Another) &lt;Spy&gt;                                                               | 7.66 | 7.96 | 8.45  | 9.01  | 9.42  |
| 1.10  | P*Light feat. mow*2 - Homeneko*Sensation (8K Lv.12) &lt;victorica_db&gt;                                            | 7.57 | 7.87 | 8.51  | 9.43  | 10.34 |
| 1.99  | S-C-U feat. Qrispy Joybox - anemone (Kawa &amp; Julie's 8K Extra) &lt;Julie&gt;                                     | 7.43 | 7.86 | 8.54  | 9.25  | 9.69  |
| 1.05  | Kaneko Chiharu - iLLness LiLin (HEAVENLY) &lt;Fresh Chicken&gt;                                                     | 7.34 | 7.91 | 8.64  | 9.38  | 9.65  |
| 1.59  | Amane - Space Time (Amane Hardcore Remix) (7K Lv.40) &lt;Lieselotte&gt;                                             | 8.07 | 8.28 | 8.73  | 9.43  | 10.00 |
| 0.97  | Ryu* - Yukizukiyo (victorica's 8K Lv.12) &lt;Spy&gt;                                                                | 8.04 | 8.25 | 8.73  | 10.50 | 11.20 |
| 2.42  | GReeeeN - Shinobi (7K Burst!) &lt;ExUsagi&gt;                                                                       | 8.23 | 8.40 | 8.74  | 9.16  | 9.49  |
| 0.77  | xi - Double Helix (Nucleic) &lt;Level 51&gt;                                                                        | 8.30 | 8.46 | 8.75  | 9.08  | 9.33  |
| 1.63  | Yooh - Ice Angel (Euphoria) &lt;pporse&gt;                                                                          | 8.24 | 8.42 | 8.76  | 9.28  | 9.71  |
| 1.34  | Ogura Yui - Baby Sweet Berry Love (3R2 Remix) (Sweetness Overload!) &lt;KawaEE&gt;                                  | 7.91 | 8.21 | 8.83  | 9.53  | 9.89  |
| 1.64  | Ryu* Vs. Sota - Go Beyond!! (7K Black Another) &lt;DE-CADE&gt;                                                      | 8.16 | 8.35 | 8.87  | 9.53  | 10.20 |
| 1.63  | void - Valedict (Black Another) &lt;pwhk&gt;                                                                        | 8.18 | 8.42 | 8.91  | 9.44  | 9.93  |
| 1.55  | Cres - End Time (Epilogue) &lt;PyaKura&gt;                                                                          | 8.23 | 8.48 | 8.92  | 9.33  | 9.68  |
| 1.10  | High Speed Music Team Sharpnel - M.A.M.A. (ExTra) &lt;arcwinolivirus&gt;                                            | 7.80 | 8.33 | 8.92  | 9.41  | 9.67  |
| 0.72  | XeoN - Xeus (LV.12 Leggendaria) &lt;My Angel Azusa&gt;                                                              | 8.35 | 8.54 | 8.97  | 9.39  | 9.66  |
| 1.20  | D(ABE3) - MANIERA (Collab Another) &lt;iJinjin&gt;                                                                  | 8.39 | 8.55 | 8.97  | 9.55  | 9.90  |
| 1.20  | orangentle / Yu_Asahina - HAELEQUIN (Extended ver.) (Jinjin's Dissociative 7K Identity Disorder) &lt;Fullerene-&gt; | 8.32 | 8.53 | 8.98  | 9.54  | 9.93  |
| 1.25  | penoreri - Everlasting Message (GRAVITY) &lt;Julie&gt;                                                              | 8.23 | 8.49 | 9.01  | 9.53  | 9.78  |
| 1.68  | Gekikara Mania - Deublithick (Blocko's Extra) &lt;_underjoy&gt;                                                     | 8.20 | 8.48 | 9.02  | 9.88  | 10.37 |
| 1.30  | Cres - End Time (Afterword) &lt;PyaKura&gt;                                                                         | 8.38 | 8.64 | 9.02  | 9.62  | 10.15 |
| 1.03  | Sisterz - Inverse World (Universe) &lt;Kyousuke-&gt;                                                                | 8.50 | 8.63 | 9.02  | 9.69  | 10.06 |
| 1.34  | w_tre respect for AT&amp;HU - Schur's Theorem (Black Another) &lt;Nivrad00&gt;                                      | 8.56 | 8.74 | 9.05  | 9.76  | 10.70 |
| 1.63  | Hermit - Dysnomia (8K Melodie de tristesse) &lt;-Kamikaze-&gt;                                                      | 8.39 | 8.61 | 9.07  | 9.80  | 10.67 |
| 1.37  | Sharlo &amp; yealina - Kakushigoto (Rumi's 7K MX) &lt;Sharlo&gt;                                                    | 8.18 | 8.46 | 9.07  | 9.76  | 10.19 |
| 1.66  | Shoujo - Reminiscing (Black Another) &lt;- R e b a -&gt;                                                            | 8.40 | 8.66 | 9.08  | 9.68  | 10.11 |
| 3.66  | xi - Happy End of the World (9K Collab Insane) &lt;Blocko&gt;                                                       | 7.88 | 8.26 | 9.08  | 10.31 | 11.10 |
| 1.25  | BlackY - Harpuia (INFINITE) &lt;Ichigaki&gt;                                                                        | 8.42 | 8.58 | 9.09  | 10.04 | 10.53 |
| 1.59  | penoreri - Preserved Valkyria (GRAVITY) &lt;Takane6&gt;                                                             | 8.10 | 8.43 | 9.09  | 9.79  | 10.21 |
| 1.10  | Yooh - LiFE Garden (Extended Mix) (Eutopia) &lt;Wonki&gt;                                                           | 8.28 | 8.48 | 9.10  | 10.53 | 11.25 |
| 1.33  | kamome sano - archive::zip (GRAVITY) &lt;Fresh Chicken&gt;                                                          | 8.29 | 8.52 | 9.10  | 9.86  | 10.34 |
| 1.12  | Soleily - Violet Soul (D's Extra) &lt;pocket-Gao&gt;                                                                | 8.41 | 8.64 | 9.12  | 9.77  | 10.46 |
| 1.67  | LeaF - LeaF Style Super*Shredder (SC) &lt;nowsmart&gt;                                                              | 8.22 | 8.61 | 9.12  | 9.64  | 10.05 |
| 1.61  | xi - Quietus Ray (Heaven) &lt;Kuo Kyoka&gt;                                                                         | 8.36 | 8.61 | 9.14  | 10.04 | 10.73 |
| 1.51  | DJ TOTTO VS TOTTO - Vajra (Emiria's 8K Leggendaria) &lt;biemote&gt;                                                 | 8.37 | 8.61 | 9.15  | 10.10 | 10.84 |
| 1.95  | Hermit - Dysnomia (D's 8K Another) &lt;-Kamikaze-&gt;                                                               | 8.39 | 8.62 | 9.16  | 10.24 | 11.04 |
| 1.58  | MiddleIsland - Achromat (7K Black Another) &lt;iJinjin&gt;                                                          | 8.52 | 8.72 | 9.18  | 9.95  | 10.41 |
| 1.19  | gmtn. (witch's slave) - furioso melodia (7K furioso maratona) &lt;Harbyter&gt;                                      | 8.19 | 8.52 | 9.20  | 10.18 | 10.88 |
| 1.58  | DJ SHARPNEL - Touch the angel (K-ON!!) &lt;pporse&gt;                                                               | 8.36 | 8.64 | 9.22  | 9.94  | 10.61 |
| 0.81  | MAZARE - Mazare Party (Ash's 6K Extra) &lt;Insp1r3&gt;                                                              | 8.28 | 8.59 | 9.23  | 9.95  | 10.30 |
| 1.87  | DJ Mashiro - Prismatic Lollipops (Lv.20) &lt;Shinzo-&gt;                                                            | 8.13 | 8.41 | 9.28  | 10.24 | 10.76 |
| 0.95  | Soleily - Renatus (Another) &lt;Multiple Creators&gt;                                                               | 8.30 | 8.57 | 9.28  | 10.09 | 10.70 |
| 1.21  | BlackY - FLOWER -SPRING Long VER.- (As Flowers Bloom And Fall) &lt;Kawawa&gt;                                       | 8.31 | 8.57 | 9.29  | 10.39 | 11.31 |
| 1.81  | Nekomata Master - Sennen no Kotowari (GRAVITY) &lt;Critical_Star&gt;                                                | 8.53 | 8.81 | 9.30  | 10.36 | 11.73 |
| 0.74  | UNDEAD CORPORATION - The Empress scream off ver (Jepetski's Empress) &lt;TheZiemniax&gt;                            | 8.12 | 8.53 | 9.31  | 9.78  | 10.02 |
| 1.37  | Team Grimoire - C18H27NO3(extend) (7K Axities) &lt;[Shana Lesus]&gt;                                                | 8.46 | 8.71 | 9.36  | 10.15 | 10.59 |
| 1.69  | Camellia as "Bang Riot" - Blastix Riotz (GRAVITY) &lt;Fresh Chicken&gt;                                             | 8.15 | 8.64 | 9.38  | 10.21 | 10.78 |
| 1.65  | Kucchi- - Remilia ~Kyuuketsuki no Tame no Kyousoukyoku (Rebanada's Black Another) &lt;Garalulu&gt;                  | 8.52 | 8.75 | 9.39  | 10.26 | 10.84 |
| 1.80  | Kucchi- - Remilia ~Kyuuketsuki no Tame no Kyousoukyoku (Concerto Cruento) &lt;Garalulu&gt;                          | 8.64 | 8.89 | 9.51  | 10.29 | 10.81 |
| 1.26  | Halozy - Kanshou no Matenrou (Eternity) &lt;Rumia-&gt;                                                              | 8.37 | 8.73 | 9.52  | 10.38 | 10.82 |
| 1.63  | xi - Garyou Tensei (Million's 7K MX) &lt;LNP-&gt;                                                                   | 8.36 | 8.70 | 9.54  | 10.46 | 10.88 |
| 1.29  | Mitsuyoshi Takenobu no Ani - Amphisbaena (Fallen Heaven) &lt;Kawawa&gt;                                             | 8.63 | 8.96 | 9.54  | 10.16 | 10.53 |
| 1.59  | Chroma - Hoshi ga Furanai Machi (Meteor Shower // pporse's 7K) &lt;Wonki&gt;                                        | 8.31 | 8.58 | 9.56  | 11.46 | 12.82 |
| 1.72  | LeaF - Alice in Misanthrope -Ensei Alice- (Alice in Wonderland) &lt;Kawawa&gt;                                      | 8.40 | 8.70 | 9.58  | 10.52 | 10.97 |
| 1.33  | Umeboshi Chazuke - Panic! Pop'n! Picnic! (Picnic!) &lt;jakads&gt;                                                   | 8.69 | 8.93 | 9.58  | 10.38 | 10.77 |
| 1.10  | xi - Ascension to Heaven (Elysium) &lt;Jinjin&gt;                                                                   | 8.82 | 9.05 | 9.65  | 10.36 | 10.73 |
| 1.57  | Ayane - Endless Tears... (CrossOver) &lt;richardfeder&gt;                                                           | 8.78 | 9.14 | 9.65  | 10.40 | 10.98 |
| 1.07  | CLIMAX of MAXX 360 - PARANOiA Revolution (Expert) &lt;Tornspirit&gt;                                                | 8.98 | 9.23 | 9.65  | 10.14 | 10.46 |
| 1.22  | Jun Kuroda + AAAA - Ultimate Fate (The Apocalypse) &lt;Kawawa&gt;                                                   | 8.59 | 8.83 | 9.67  | 10.70 | 11.22 |
| 1.35  | Warak - REANIMATE (Reanimated obj. Kamikaze) &lt;Rayz141&gt;                                                        | 8.58 | 9.00 | 9.69  | 10.70 | 11.46 |
| 1.29  | Ice - citanLu (pporse's Lunatic) &lt;Lass&gt;                                                                       | 8.72 | 9.01 | 9.69  | 10.62 | 11.20 |
| 1.28  | Yooh - FIRE FIRE -DARK BLAZE REMIX- (GRAVITY) &lt;Shinzo-&gt;                                                       | 8.83 | 9.07 | 9.72  | 10.53 | 10.94 |
| 1.55  | xi - Happy End of the World (ajee's 5K Armageddon) &lt;Blocko&gt;                                                   | 8.74 | 9.10 | 9.75  | 10.45 | 10.92 |
| 1.74  | m108 - * Crow Solace * (KK's 7K Extra) &lt;Critical_Star&gt;                                                        | 8.60 | 8.93 | 9.79  | 10.95 | 11.49 |
| 1.22  | Cardboard Box - The Limit Does Not Exist (Extra) &lt;iJinjin&gt;                                                    | 9.05 | 9.25 | 9.79  | 10.33 | 10.61 |
| 1.63  | DragonForce - Symphony of the Night (Rhapsody of the Warriors // 6K) &lt;ajeemaniz&gt;                              | 8.65 | 9.00 | 9.86  | 11.18 | 12.12 |
| 1.97  | xi - F (X) &lt;pwhk&gt;                                                                                             | 8.69 | 8.92 | 9.88  | 11.65 | 12.98 |
| 1.89  | DJ Genki VS Camellia feat. moimoi - YELL! (Solitude) &lt;Turrim&gt;                                                 | 8.57 | 8.93 | 9.91  | 11.48 | 12.39 |
| 0.94  | Gekikara Mania - Deublithick (Ultra) &lt;_underjoy&gt;                                                              | 8.43 | 8.77 | 9.93  | 11.32 | 12.35 |
| 1.14  | KRUX - Illusion of Inflict (7K Kruxified) &lt;Reba&gt;                                                              | 8.58 | 8.93 | 9.98  | 11.80 | 12.26 |
| 1.22  | Toromaru - Enigma (GRAVITY) &lt;Kawawa&gt;                                                                          | 8.86 | 9.20 | 10.02 | 10.96 | 11.57 |
| 1.46  | sakuzyo - AXION (Ex-ray) &lt;ljqandylee&gt;                                                                         | 8.81 | 9.13 | 10.02 | 10.88 | 11.41 |
| 1.53  | xi - Garyou Tensei (Million's 7K SC) &lt;LNP-&gt;                                                                   | 9.07 | 9.45 | 10.06 | 11.03 | 11.70 |
| 1.92  | DJ Genki vs. Camellia feat. moimoi - Sunshine (7K Luminescence) &lt;Turrim&gt;                                      | 8.79 | 9.16 | 10.06 | 12.07 | 14.42 |
