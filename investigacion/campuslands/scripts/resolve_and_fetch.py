import os
import re
import json
import urllib.request
import ssl
from concurrent.futures import ThreadPoolExecutor

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,application/json,*/*;q=0.8",
    "Accept-Language": "es-CO,es;q=0.9,en;q=0.8"
}

OUT_DIR = r"c:\Users\tomas\second-brain\sources\prensa_y_web"

REDIRECT_URLS = [
    # El Pais
    ("elpais_1", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFj51mU9Bo69bd_yo4jDRLQSDKab-k68q9QzQbf-g4NoYH6g9_3_Ud2h6vEQ6rxWc6-dUWQTox4q0aQElfluIep00o1GXHE93GOU72zBYj_FTLxGT4gN67x5GTqsYoU0PZuon_qhorDlsKlfpgFAPNsdx1Zh33zm9lnq-71IkrpZniVpgECm3ueINO7ZNTHN5LfvK14su9yyVGcIaoZ7837CwFzoEkOZMiEnCESJ5s4YC2DrRZe"),
    ("elpais_2", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQErUVLfvDsIyMuZSbg3dQVoVwAWx0oeeM0-_sTZwiu-82DuCCKVtCK1F3KdUsrlpRZByot9OftQhcgkW3rXRGH3a_QSIq3n93poyVIjmtbiVUnPcD7iZqGYyhmW8Sy_2tpxP9BMlElo7wg="),
    # Bancolombia & Zona Franca & Includere
    ("zonafranca_1", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFgPaBHx3AeJMpfubCZ6x-TaEWZr8V5QYLPTUCZKtrEzPCkZjDkjD1XXIf0So_QnQoG6PKq17-yuS7PTf---6hGAPFeKm-EsMeYuQwZYznDh27s6RFTBjBISRoYeOYRxLy818Csi70CLWCoSpUeHZ2OSxKtSw=="),
    ("zonafranca_2", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQESHa4FN0Hzua8Cvu2phFCpeP52Lwmd07Mb5Hsefp9-yYYJNw3K2Rff8wRpHvHHnmrKYlF2iMdKAUQfWpf07AHAQo8w5mW9adWi1NV-LoVzv-DCBLA9fp9TIurHMuM7q5ZP7D10POW1Vo0-k1ED90ZMQQIXT6pNdb0pSM6BD7Q="),
    ("includere_1", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHh7BaDrJTNkD7RV3SBwrxHbOWu43Vnih00RQFnPF7qV3L4YPXZP6iiifHlBn5vpavDBkHvkIt8tI3Xb01nEE_LeArnjJA1B4ECyG4-bN-PwoX_2jrQ4H-9nCm0roLzE8ZkjqOGreqPcpmF3xC_CkUW6a1ayjzGVJVfqv9sGiEG18RU8Fmn5Q_JxUU38O4="),
    ("bancolombia_1", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQG8WFaD6m3Rz4BU3vDFAMZj_Co6eqQ87q1dMMTe__GS0t_RpqvVOi7g7ygxe-c2ibd4-wVt8skUzuIxuV38CnRTJoFyiaXvuq1Cg2suwrmbqPyveKfTy21QA7sub_wOJC8RsadIztWPYg=="),
    # Fedesoft & MinTIC & Senal Colombia & Las Ciudades del Futuro
    ("fedesoft_1", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQH75sIdStLtR52gRCQMrBHHAEhZAKel4ZhuyHH6KShF_ft5LH3PBz43Yf9uq0S-E-72NMedEmLonMsr5yhdGIKVjnHZhRLool1dt1N97IufFvADFSYGTSExry4="),
    ("fedesoft_2", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHt3Tc9pqV11U8PsUBLmIT15IbLmu2iNvVCI0shNeqdAUjjojV2PyyIwbuHf7dW0a7hjfOgevh3s3WdAhZYe3bs-evY0jXNEsaHie_rrjMHSd1I"),
    ("fedesoft_3", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQH9LaZEQovaVnbbcwmnuAzpCzk_L7p7AGnhOYMlpAd0sGOw7-YfUic0z6UX2KhTCseJeJCt2aOmGPqJR0491a_6i_viSW_3MOxStER2dYW77fEHncoyhmproAkyDoxT-5dWtesq6hu2tZU="),
    ("fedesoft_4", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQE13iKESN2zjtlbcPhleHwA2FGe6FZl_fEP_dZ1mWk4jKS_3eITYEH9ETrP3C5_-D4eegxG9Lf5F_ZS6HszAAgcT-COD9i6-Xc8s3vqOUX9tvP7vY6vKrEUHkXUFbFFuI73U-uu7xqgs13frxQO3PhlokRT-NY4FhUGVgB33cRJaFvmpnA5e7ia3jt30gwtc6bJf5e2JFkjp6n7dXF7STBl2YZ8YYSThqXjHQ=="),
    ("fedesoft_5", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFZ_YfJB41lV2pdMWemfChDrIDuAceB7Bt_ThtX4v7SNNVCjj2VsJJgxe860QJnlD8i0bDnJr8f-rS1CzKdjM4tH2xENovh8C2juctZrahmObV9DFGa7tNb4a269IfePdSrcOiu4fVjfBilvtGKrBCl5Lzlca_B2tw1xzwbftO-bGvl_2djbmydRtI0Hs3mXC3N4EyBC_5qzVsJHQm5"),
    ("senalcolombia_1", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQE5m-Ff_TNNRdIpPHOY-mKri5ZT09CBG77dmzus3cuAPnXIgWdcoGm1bo4s8Vvkt1qLkIE_CCXk7W4bonEzRtl73gpeu9n4fOIi4xNn-AgqkOyWId7u_RbBNM9aoUex2RoQEuDsg0Ri"),
    ("ciudadesfuturo_1", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHSzfbbqKKOXMDb5pQIizbTFiAZRJdi-RNDd35imaoGDCjQkPRsyTMAfZra20FxcCc2JEPifzoR3AGX8jtgp3zkkiCg8xpK9TaHetC8aX-DJSBXbL1J8sFvYJO-TWWfP7m11Kwjm7_jFql8gEDMV7g7g3w0PmZss7YBBMCmIKNAWy4rIjg9lpfalxRNO6uRwhwhhF58-B8AyWOqsE9WwDkR-eUoTg=="),
    ("mintic_1", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHEwqZm5bXMwrKe3qIoKUmCeZ8aZHAB-lkm7vD8La5sxEB23KsRZXRMd8TvRZqhMFtWWJ7VuWChUNprvLm3YBoAkeJnZGn0GzjQmXXeBUF_4nXnNI3EL7y_3Y7TmP7GC8-mr_aGvB6__zqN5fcGe3L4OQ=="),
    ("mintic_2", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFY8Jkh3TBI_6EhtTm7S9oYlcfkUKnZ8g7-XqHviLLAMJoJWOY1i3663jK12xT1mpSkoyRRLJaY2ijjS1zQfNrvIdkkH60Mgf_SvDXIQp5FA8WrFqocdbUsHOoz3Yd-Ydoiztga3y2IY-ZWH1vM9aNctQ=="),
    ("mintic_3", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFdqCWRkSbN4OdcnbKg2L4jF5WDVZMAUY1ft9ZZk1oN5_Umw3BihF_lXL737f0cq9DCr87BnsSbgiIqfAB0nwQHq1d-upf_E6iu5KZR42wM3FO6tSqKM_3UL4OQVDrmcqsuyXUCbXu-hwtTHJGvVCaRltC66l3nRbk="),
    ("mintic_4", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGuYmYqnW8BTMl11pEsxo9O79MTQKDgyjItK81mCPRnJKxDbqSHan-1s0I0MLWzPRg2IIFQ1FThYFiL6bK2alJj3G7SGWFpo5PznCBDjuL1r7HsR8nXfNke89-JeG5SsdSALk1JO0hJWEC5HdoxVc4t1w=="),
    # Corporate registries
    ("larepublica_nit", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEsbblHxUGo2RbrBk5gCfMzIJrNAd1vvDoK5W46zvvwQuMH6gKnrHjYHkZThSh1lhTce5_8SXC3d3UF0evDZE3oqWQ-rmg1G8yFchblsOHgv9tD2GxOAkMLuhITgrLenTG5RwEHw9EvdHckWoSwBUbqe_vP8Kvg3_Dfc4TAxWykiQyTeYNOUbSnwlZUk8IO5ulRNM1K7DhXica69KOVyZFn"),
    ("registronit_1", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHDwvWTkYg-cy-AzOFcQ7ee0ooeuSZHIE7V4HEqQEsG5uc_NOq0WDstHGt-2cQfN5r-E9S5xS4LkVulAdbUjmUB9XBVHE5rxuGFk_qqh28xbJBqiwDQsiOayjat-dvAoMstth0476nLcp7D1FFAbOp6kvTFVD8IQstV"),
    ("informacolombia_1", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEiwtGfWFGm5yR25sCpCeSFEHGjG_H_-_ahjQm6aSEycAjEWPRU92eFkLdMtbr8C46xMWvrmCG--xYIoLQ9A3M017oWRqVvccejwMsFi7jVrSXreMJnwyoHe4qmshhndoOBd0AZakeKw2gaaXIZk02MIwUoXHAdXA6XD3rYFPbtVPmDX3M6us_oFKTzBKsDvxw9170iIOmYefBi3xTG"),
    ("datacredito_1", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFVyRoC3E9uLXWkdORfX34C7ekTS6Mm80RFFhZbfgCA4pl5IihRm1QGLYAK5OnH9JE2jrfQuCdPjSg-x_DB4EVRrjKKgqJosNVIkXjWeTBjcO5OxkyY3r9VY-4D1pPZT7gl9moGKQG9tGN6moEeCpEXo7Ho1-N44hnFDdYNlyQLGA=="),
    ("einforma_1", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQExnNbi7nqr9kCVQYYHNnEcMv_fVLPBaUEogzA_5bqCkm6JioEBspXn93acrqfXmAlhbZ-ILUs2_LMWINUK4EhdgaSgAoBUZpbA9TS17rg2jFR7oAaVZ1dur_4="),
    ("societeinfo_1", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQE3Fuf_WKU8yD5P1o3yDZtMYyUB498EtmxCv4UHaKRjS9K2zy_7zqcB1fSP3JYufGF-PW199fHDMjyd7ykdx9n5jflGetBiBP5Um4nGTzTOdk3iqfoN_pHtZAecRhEGUD2ecjWovb_QvJprpCoH"),
    # Reddit & Computrabajo & Magneto
    ("reddit_1", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFly0RN395BYlWZQrJut6Bz-aQSGJfm2ESgglyPbzQUX0Xa5w4Nyh8Y5T9ugcoTjpbgnVqmyRsCsKimVnX41Rg_YYse_5wMJ1mt3kKCuJANRKS5FbEH9QAGh9Ybq8swTMzgzVbvJAAzQanAhJL6H01z5t-MemRAsrAfBEV2RsOGyJgmgARlnmz69tb7EQDwug1ymevKBVV-Luj01M0="),
    ("reddit_2", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEzHXK61gXxzPrv_fK8D7hQyPQ9P-BJKcTyxMwM-LpSOzMICFW48ugIAYkcSz1K_akLcd_y9hupLKhPjAl8jQ4wkEOd7kInXeTZE3mX42GpTukw-Uk-XFAj9dSHB_Lv7hhj8cOmx1UftHsDy_OI-J_L5mpHAGUbTL5q-m7I6EuC47oP-8EbgY4gjjRyGiKvs7Lxtx3euNbTz1I-0sc="),
    ("reddit_3", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQF2Si-D9dUgbtgVODZ8YOWkwucN2YpK-kY1bK1lBESVvm2t42I4JFSVZrKf4yedWnz6L_S6okuoKI7UopaLA_i71lPVCUGbKnF3ccBPJRl--Dsc7eOtfCTH7XjMKViz8I1pDDwkjer9nuwTZMyjK9cS0-1LKKRJhzxEBsP3G7o67JNf8DfHGF4bUl1vxq7pF9ZxVg89PvjrR9_y5A=="),
    ("reddit_4", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGL7KrzC4yHlqC1J7cfnwnF6l47RCpeYytN2BeEd51uw7wNE7Awk5l8CwretsopXUaoZ--ha-8gfICVcshzNMcwBCLhfZEMKykrhw7sqBrBAqvUfY6tdPo-tcfztCqPWAxIGPMsa3WcHigg8yJUbSfR6Zisks6s"),
    ("reddit_5", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQElRulZK1YBwlNB7Eaen7hrXHI3-uT1nzZzWb2KCadSbHDUu6v9ec1EkQ05aSPwh_p7KKAXSJc8bLKZImCxx-IIBUvrGGnZ7sqtnIRdzNsSBNDf3wE0-f1Wflg3inBd1womFHrJqvHGPb9CeEZf7tKuKh8-7lNI_bSGI332hbGZMzepueYPMA=="),
    ("reddit_6", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQE8j_alO385cu9uUUcVjPyNGaQg0waQ7h0g_EMltdGpJ5MRCH4Pkxc8HY9EYJw79OxuRoV8w7w1WzDEBOgFh0TC8xN5OM7SA2tRWFQIxZAZMTcXpH_2ncFscnuTO29xtZrZh-lxf22nOdLrQHwAa0AuGmxoH6Pzyx_dy8dNwwl93D1JqKH4AQfBHquhGB3ZbfMlQA_Ghea73vGyjOw="),
    ("reddit_7", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFm6MzSJ1HLAaHkqFTuRKppa6TacU4NkArFxr25qkPEgqL08xThbUlJitzRLZGT_1VL_7P41IOVwyNOVW6-4VU0u13sXNtNBUiMMqrw2PpDv_KMvAfSxCrUYK9Noa7ABUvfyq4YHQOqkW1ze6SkgW1q1_5RFwgZ9iJwAlbKruGtn9b021XK1Yk="),
    ("reddit_8", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHyG-BuV2eI-qI4UH-yfBqjD54Z5DkC-q4hpgcaPodxqsS7vqqSBPWWYQ_evJ48JSKCn7dmHGHdH7A_cR8CDNFFW5bOFExfZO2mYagG0ACeAEjWJiDe7n3Tu1sGZTpeh6SWfE2IhfnkztKj55AfBS3spm-D1eDjHA=="),
    ("computrabajo_1", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFHFUUeZOmTEGTm3zGc4YHCJopBo6e6RS1Ek5i1KOfJHVB1bbnUg2eAfSLa6J3-v5jtN-XG33gEEI85vZWg4LSJNLeARDZhGzs0WM3INuW2ljqDUQTOV3BClgGf1iPsQeYBXkQNlkw14QM1gp7IcNpzvCOjzsiSLYUXDp6PhHeXH6U="),
    ("computrabajo_2", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFhEeNJ3jI1NqmASkBN_w8cvwwfDMhkNlDwlyFVcI3dlYf0-UrNA6Jll2bUmPFj5UHF0H1ZBA0Jo0tvkN9FxW760cfJcTAuoAwmJjjObv8giMPGx5Vn6nVdOOZ4o2mc71ZdGRwCcUxf2F8dyU116ogtJnrdxnOIaAFVqMCnL8M3CFo="),
    ("magneto_hubux", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQG4IH7GAzfKY4Q-FH4_9X9zUPT8xr7uIsIRNV_vfX-5jfB_Op3wR7Xg9FYPVRQAYYReeI77o6vlqmrGLoxvl54ucJUkpy14JFj9sY_lklgQxwU1JEivPsLBYHxFJFfH1Ym8DC6LgdcWijhe12yfakVN5igvIGU1MqujHYBSd7uLhEZZmOlfd5bg"),
    # Uniminuto, Semana, Prosantander, EAN, Educacolombia, Cajasan, Forem
    ("uniminuto_1", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHVg-uQuhEQKBHxJDH6419bEEBZL6jRGgvDzVxN7XuxpPw6sqoyS2PjH_eGqlM3Xw_2zTr0ZyiXvGLSJpnG2w9EQ8xrliwOA0stX0HLaFZQyjx0zewFgv1-iJa3RXWl0dhdAMwFOQvQtBhIojZ5gccqy8owEVwGnNkkv3e7xoLDnFfoV_vCa722juk67J7sD4FZX-QsJjZ89AASp9Sofr551My0ozqXxGMEG9I="),
    ("uniminuto_2", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEA3u6GQB1neGShnJRBOq6-88Vgr2PbSqZjZ1eNTdlIuIuFsxpZLCXqpdl5NFvuXDTqaSXxNS9LKnLILt7LvDTeh0KJ3tnuNEeRT5_X53Yu_qR-IEm48-4Lk7cZqi_Ln9h_vcfimp-VFNoLuE763QaANeSsLZgLEBqX-TZ4t13SSQ169CnLVDQ4dELqmCj6bIg3TRNmFO1P2VOFFqpSftSDtyJdnlTOQjuHPWKL"),
    ("semana_1", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFLYzx-xLL5l5--NDAjqiPKxtmJyUj1jyJOI8IC7iJZ_TumD40vhLvSzuDnste_n9Hz5YS-JuTbwHoGlM4Jv_G1wzvQksU6FXBUZhlLHUdN72iyZckr6h_LYN1Paf2glGx3C2DGNkWhThBJtd-FOTl2Amp-_0mRuSMmEmK6QSWWbNHbT-QGJupZOpIkSTAmB2SfmFqY1N-09Ma_TznFJH3GdtIhDiIVGtc7TlU="),
    ("semana_2", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFm9H6qgSeoX29_8g67_VLUvXguRr7fgKsdtRq_RJbImaypO09WRf3LW8NYw1k-L14kZ98notSOU2NaJ_mBoyBrgvejZlLOkm8hiHwAbTFOuB9pQFDz0pj4AGV7MAba2EPA4v1baKBooBLUtrqlEEH834viPt9NjmDEtGKoTAt2G6XeiqNyA3ykF44YkIPKP6L_pmEPlTQWhxgqth0apcAdSbfztd2jtgpu_c2HPNRBRG1-byD7SOyz0YzWfC3l4yQN"),
    ("prosantander_1", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEc4z1n5bjvnq08FFjpl1YLddsAQxesLZaL9tXkzbYr9XPsYia23uUTPH2nrr_v6ujDHedGRrpaAc2WTPzuqzp1zAG0a3kxnraI1IjPSDumEBstG4U-8pAk9PQ-3_LLUyQv54IeHU-S_jszrcW8GAU0yKa7pA=="),
    ("prosantander_2", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGewDgDF7qr-Odn_u_G6csTnJFiKRheC-4FUq4z7iJToVe073aBiiEz3Ay6M0LGekeDMv7aAsWRWrrdMjvfwgcwLnGAWnYBvydopAYIfuNXBNND_e75i_f_OgaLkEolDiLw_Um_J2ciE77FG5k9jeoDkk85SRgmB0kSTkSPfZYFKZvLYg-xqyBDBSEySSX_XIV4"),
    ("educacolombia_ean", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQG-FRWXqNjX7mjAG9oiocnEvS60NASXW6xK09z3Uwno96cWRD_bc4Dq798fY2LaKWdz4Zn8VXl7XirhguYxBnRzgzpgG2Nv0MHcm-BK2njWW7wsZLpmF7O_-7wOFzoEAvyM2nb0Qaw_9TDmw9VYUznjT7BB"),
    ("cajasan_1", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFQ98gKa48fToj116rqRkl3QWx6s-uwzldcRq0vs5vCn2jHQ_mxpXGS83RVdxNKwYB5GhI7J-6IAcHl6NvhgdwhursrzSYH9V-b0NhkQeTpxJ8NlSa-Pt6YsZf0NbLCmHQEYV6qskVoylJ6et739pR41-0Npm3MVwm3VDj3jfPfthQARLtlOr8S0Co8NJSSXQ0="),
    ("cajasan_2", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQG1w3bYI9eiskpaciQVqRrcM-0vW6dL455kfhlFoMnBGAciR5VSlTXroI3jjbzZtbLaQzj_xcYjM6A4BMZ8m94ytinD1dBWVGMZl_xWubad1vrO"),
    ("forem_1", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGbzqhb5XvC0POCdUTLdY2Y3JyIV97_nKs6fsyVIB_u6Djbu2DEGc-QRdJG9t4EuL4T1Gto_jZ8Wbx6mysuUyCGfwzpfSCluKyZYJvZaGQ="),
    # Grupo Bien Pensado, Leeche, Camara de Comercio, ConnectAmericas, MadeInSantander
    ("camaradirecta_1", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQG_y8mZLvqJWNdmqBjxyaP1bbcNj6_sBVvsC1tPsWCZMBYa5dHIQGDTBHTl8cgT_bz-qH5uA5M9ExF1kNyQrKgR4opzT0VcRIA8LxofkG_Fz7sl-xI8yyzKyWVezLkMoX7waIDHvLFPbMnLoI-oodDlHA6l_ckk-VYFZeLeWdGq8kzNWnZo8J8j"),
    ("camaradirecta_2", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQG2ETbV7r7NSgMoFRXTOIeBNEyNVSwDCH5dFTBvIzDgGhFWVt5p1gLO6BdFmDpgVPIO7GJHmFzfdouo8QDHpHUkVbIuxaZQZ10zqjn09DH9CrJqhv7mDi_2rgF7GvbccapsYyvuqdYu5ucWRyh8X1ITrXN5sLj7TO6Rcjy9sjjb8Kfa8Vi4NPjPzEaEJUx2UbP_xBle7TmhhLVeskzsTG49iUODdeRtDfGyxAxedXcLl6mr2GA-ZIQ2VvvQ3TooKzEmu1qZ6A=="),
    ("camaradirecta_3", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGXfrmzcVEVsHNEr6EVt2xVYeyPKUfbXZvzoQMkS0xOfDJYWxdSJ0DIMvsrNZp5qTKAkqTxq97c49Myqp3BBZUvJesF1m97EPXzAW0vov-VvyOTJB0NjSP6YaTJ32fwcoTGwa71OVJDpM2f43WxBs1FVy_vCWPvjlV4Vn0FsnlbgdGplSm9hC3fALnex40RdFRbyDHWoakbhwQBNWdHApf5IBVMIkhfegQlSyLqS38cG_eYLc1unqf40rWf6Q6zly3ORwu2QAAxGQ=="),
    ("connectamericas_1", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEFLcnht79ciCVFMAt5tcNk1CSv4oZ5vMWSHZx7g4-6wV9hZjzjL_Ihcy2mLFBuDq2la1m4ipoN_TIYYa4tiFeA2xoUYeuXnPBvgdHs3E4B1VBUtwUQjGR9IUS_bH-v7WpYySd0D-GU7Usaf1srCoq2GpMew5QoO2opHIQ9OEoWVv4VEmtIKgoXXKq0XziZw9v3V58="),
    ("madeinsantander_1", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEmwBx28Ai2XsaOa4KCQZPMOmG_HPVm6O7Yl3wUtIC873nuQVWeKxYnH9kfAFNfSThqPyajyK_o92hbtPy2jNgPQ-2mBm2zNu5TvlR3ab09qWqG6bIJFh6xrntQPfZoGWck-3unlvg2hxSBblszvGHYVwQBJXj4"),
    ("vanguardia_leeche", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHNJ-vY-aoAqwmGIwxOinyOlI-Wl-VnSZ-NAkEHAo9ks3XnEeduZJDSx-FQ69Xe9g7IyqpGt_wP9bK4ViU2CD-vvIkVIy1eDR4M-tF0qH_bWYU5GRiXFjb9Kb6-e1-cLDUAvOuYJ3OMtArwBeGmM82qyx-HgNjw3jdBhXXEijSlGZl8bzIR9Om90pspKOQpZv52va8o8xi-6JtXI-0l5hT0"),
    ("portafolio_gbp", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHHQbp5sUGTD8rdbymCgslqQQDCIToosy2CKaZjWDznckpHkDWMEHb1avVuYjtSNTxAtN4Orn8LTrFeY85SGlGOKdRQ0qnVszVUiEiOcyZ5EKSfv5I3SUf9SHshCELBvnSlYIFQy6Y7M-kEvcavEbwT"),
    # Guatemala & International & AmCham & iNNpulsa & Alcaldia
    ("campuslands_pro_1", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEwf9gSVmEsH79qzkWBEXF4DSMjFwWkb4u8CqmPv44JK0mx3vKKL7Z1tPiuFaEO3swJ_lqTIuuwQPul-LB4XiK4QZLFkSJICekiPjyqz7zRF7I="),
    ("canalantigua_1", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGgeqVV7D_eXuhNzGWbV-psm4XXnDKg9Tg6w0xkeJZqVGnceKhizHVAwJGBUmHNo1vrMYcFnOVjt9bGTcZNXLWIoBGaArg7D_w612F5ovjqPQ4zMjdUHXhvusNJ2qulCOlktWCAbwtV8V6t6r7wni2BrRqpG8IVBaf9rUSq3Nu29XxX-VPHXeOM0NWIz9dGzJ5gj6KXuu-gPlvj2QYuixVMF2KF7bRrY6w="),
    ("prensalibre_1", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFar6fXvPk00Qc_mDtr1tkB9ezzxNKGCIu6Y8-bdETHd1_55WVTIBiZLEhZPLJuqKzKPKWt18KiBcfggfetUShRINXFtkcl_XBAqplEX_6rrrqU236D2xx8xZ0669o9y7_WChc="),
    ("bucaramanga_gov_1", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFtlFNprai621EiS4aax1xCsXUyZywKvYjd17OUei4w6GVsnSE2dogepIKkohXfHNCKC0fTh71VG8S2M7ID8r2vQn9QsFLKwsjUPrGvqLu8EzF4p0kBXvTv1w0PUhwtulW-j3CFTbDvGUXvj7csLBfrpeIOzbwuOPfAwhJXUefZRTAVLV8o3w=="),
    ("bucaramanga_gov_2", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQE5Ie9aJxA8vSt83g8EA_lsnalYKmAOUSvTMhIsF_fXm1_juQdUOUSOqRjAN57Au2w9OhUT_SLr-NNFN0x6boO4uRKvuTw-sfdi7USPUiaysR3XzVbi_P047yp4Df-GQAaK_crzTDa_XXBkQ_k7Zytiw9oQsHG0QunZLbzmHJCTslj39B0YK6kxuROhileNqpigPkZrCDvExdF2FIrFrtHljFlrwP4="),
    ("amcham_1", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHfPaXMPI8n0MGNvwGsa1-E_PLmz7xyZid2iHdIt6PrUDIMPFHaBtlsebz7yXzk6ow3DVFUSCjv0pmxsui9L2fUEJbnhYiqTzG9f76xPOpmLkxVQdj34yvfU_pJnoPYJz3dAiYkWYuj6UrCtR5-vTCRQtT2maOfJyWvF7TZ1fJORiHud8csbYy5D4On1gSt9UJRbTcIXPGSHYmrjve3W3KGeYtgZObpSBZQ5B4c4MR9dK8nWz5o7REMWcXduvKSqxV3ECTjxoA8-Kux-4SVpH-BWO-wZUT1z9fETB4Ms2yoGUIEHe9mn1MMMN8_IJ---4ls"),
    ("innpulsa_1", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEOS_Nx7XmX-hqTB6F5IC9TTGElXwocCy9Dx_Ad_perBuflLaxSs-204t9V03bo3tJJOQTOhSaqx_ZwFOl8xpy6j_nOncWiC7btI0uEpDdsI-dbVBbMqhowQdyJrySauVn_s0hKt-fwVXmknuEIScZ2mnxE2auk5PnqUwB-kzvo-ZL3LWcxSUVQB4Z7rL35_gZ-KranOZgJIxNI7unZQOATryo08lfCS66gc2tWTx8pmyJ5pnfOc4iZcFm8NoN7BunRFQWw"),
    # Campuslands subpages discovered in search
    ("campus_sub_1", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGUcYF-G91kQx6bnM7Ad53x09wUBrCKmwlSWn-DuOaspooUOlAIV-mYHvkJ-YW793VSfs2qhXfdxp2HGF4IKgxvv_TjPypTqAzEQPOK6mHwVeZKD8XP"),
    ("campus_sub_2", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHTFjQeK0KQ_p5s50aZkjIut9N1BLOoY5-rDbjEs9OvkMN51n8gnzG7HRP0IHg3DaU9zyO7GfmG5TEdgpDn5_gcBjlWgo0LzpCOdp6bKbD2GiFnBOEyoG3h9ptqwYe7xw=="),
    ("campus_sub_3", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFr0qKO13rysNCGbjv2h6mqITfvb_bgH5CqthnwXt_vxWxO2vd9zOhC_SpdNKRVkpWwi-6ad5Ar4ED7di8Edkc6vgciVWuRpM8hwPRtB2WdNta7mo4JB9Zf2LuFq2Q="),
    # Existing press articles to save full text
    ("vanguardia_2023_02", "https://www.vanguardia.com/economia/local/2023/02/05/entrevista-colombia-necesita-150-mil-programadores-y-en-santander-se-entrenan-mil-diego-tarazona/"),
    ("vanguardia_2023_12", "https://www.vanguardia.com/area-metropolitana/bucaramanga/el-santandereano-que-fue-elegido-como-uno-de-los-75-nuevos-lideres-que-transforman-a-colombia-MN8186529"),
    ("vanguardia_2025_10_07", "https://www.vanguardia.com/area-metropolitana/bucaramanga/2025/10/07/santander-formara-gratis-a-200-jovenes-en-programacion-y-en-ingles/"),
    ("vanguardia_2025_10_21", "https://www.vanguardia.com/economia/500-empresas-generadoras/liderazgo/2025/10/21/reclutar-sin-sesgos-la-apuesta-tecnologica-de-las-empresas/"),
    ("vanguardia_2025_10_31", "https://www.vanguardia.com/mundo/2025/10/31/campuslands-inaugura-un-campus-tecnologico-en-guatemala-con-sello-bumangues/"),
    ("metropolitano_2026_10_09", "https://metropolitano.com.co/adoptar-inteligencia-artificial-es-cuestion-de-supervivencia-para-las-empresas-diego-tarazona-ceo-de-campuslands/"),
    ("metropolitano_2026_04_24", "https://metropolitano.com.co/campuslands-generara-400-empleos-en-tecnologia-en-bucaramanga/"),
    ("metropolitano_2025_10_07", "https://metropolitano.com.co/gobernacion-firma-convenio-con-campuslands-para-formacion-de-200-jovenes-programadores/"),
    ("eltiempo_2025_10_30", "https://www.eltiempo.com/tecnosfera/novedades-tecnologia/empresa-tecnologica-colombiana-llega-a-guatemala-y-amplia-su-cubrimiento-en-la-region-3504721"),
    ("portafolio_2025_10_30", "https://www.portafolio.co/tecnologia/campuslands-se-expande-y-aterriza-en-guatemala-para-posicionarse-como-referente-tecnologico-482440"),
    ("elfrente_2025_10_08", "https://elfrente.com.co/jovenes-impulsan-su-talento-digital-con-campuslands-y-la-gobernacion-2/"),
    ("santander_gov_2025_10_07", "https://santander.gov.co/publicaciones/11140/gobernador-aspas-y-campuslands-firman-convenio-que-impulsa-a-200-jovenes-santandereanos/"),
    ("laopinion_2023_11_27", "https://laopinion.co/premium/economia/campuslands-llega-tibu-y-busca-que-jovenes-salgan-de-la-pobreza"),
    ("diariodelsur_430410", "https://www.diariodelsur.com.co/?p=430410"),
    ("hsbnoticias_275311", "https://www.hsbnoticias.com/?p=275311")
]

def clean_html(html):
    t = re.sub(r"<script[^>]*>.*?</script>", " ", html, flags=re.DOTALL | re.IGNORECASE)
    t = re.sub(r"<style[^>]*>.*?</style>", " ", t, flags=re.DOTALL | re.IGNORECASE)
    t = re.sub(r"<[^>]+>", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t

def process_item(item):
    key, url = item
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=15, context=ctx) as resp:
            final_url = resp.geturl()
            raw = resp.read()
            text = raw.decode("utf-8", errors="replace")
            clean = clean_html(text)
            # Save individual text file in OUT_DIR
            with open(os.path.join(OUT_DIR, f"art_{key}.txt"), "w", encoding="utf-8") as f:
                f.write(f"KEY: {key}\nORIGINAL_URL: {url}\nFINAL_URL: {final_url}\nSTATUS: {resp.status}\n\n{clean}")
            return {"key": key, "final_url": final_url, "status": resp.status, "len": len(clean), "snippet": clean[:1500]}
    except urllib.error.HTTPError as he:
        return {"key": key, "final_url": he.geturl(), "status": he.code, "error": str(he)}
    except Exception as e:
        return {"key": key, "final_url": url, "status": 0, "error": str(e)}

with ThreadPoolExecutor(max_workers=10) as ex:
    results = list(ex.map(process_item, REDIRECT_URLS))

with open(os.path.join(OUT_DIR, "resolved_articles_index.json"), "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

# Also for any Reddit final_url found, try fetching its .json via old.reddit.com or api.reddit.com with a custom User-Agent
reddit_urls = set()
for r in results:
    fu = r.get("final_url", "")
    if "reddit.com" in fu and "/comments/" in fu:
        base_r = fu.split("?")[0].rstrip("/")
        reddit_urls.add(base_r)

reddit_parsed = {}
for ru in sorted(reddit_urls):
    json_u = ru + ".json?limit=200"
    try:
        req = urllib.request.Request(json_u, headers={
            "User-Agent": "windows:com.osint.researcher:v2.1 (by /u/osint_research_bot)",
            "Accept": "application/json"
        })
        with urllib.request.urlopen(req, timeout=15, context=ctx) as resp:
            tdata = json.loads(resp.read().decode("utf-8", errors="replace"))
            if isinstance(tdata, list) and len(tdata) > 0:
                post = tdata[0]["data"]["children"][0]["data"]
                comments = []
                if len(tdata) > 1:
                    def walk_c(children):
                        for c in children:
                            cd = c.get("data", {})
                            if cd.get("body"):
                                comments.append({
                                    "author": cd.get("author"),
                                    "score": cd.get("score"),
                                    "created_utc": cd.get("created_utc"),
                                    "body": cd.get("body")
                                })
                            rep = cd.get("replies")
                            if isinstance(rep, dict):
                                walk_c(rep.get("data", {}).get("children", []))
                    walk_c(tdata[1]["data"]["children"])
                reddit_parsed[ru] = {
                    "title": post.get("title"),
                    "subreddit": post.get("subreddit_name_prefixed"),
                    "author": post.get("author"),
                    "created_utc": post.get("created_utc"),
                    "score": post.get("score"),
                    "selftext": post.get("selftext"),
                    "comments": comments
                }
    except Exception as e:
        reddit_parsed[ru] = {"error": str(e)}

with open(os.path.join(OUT_DIR, "reddit_resolved_threads.json"), "w", encoding="utf-8") as f:
    json.dump(reddit_parsed, f, ensure_ascii=False, indent=2)

print(f"Processed {len(results)} URLs and {len(reddit_parsed)} Reddit threads.")
