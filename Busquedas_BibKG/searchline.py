#problem lines:

#642511

#j_mansci_ZhuKX06 :Article mdate:"2020-06-30" name:"The Process of Innovation Assimilation by Firms in Different Countries: A Technology Diffusion Perspective on E-Business." pages:"1557-1576" year:2006 volume:52 number:10 ee:"https://doi.org/10.1287/mnsc.1050.0487" abstract:"This paper extends our previous studies on the assimilation of Internet-based e-business innovations by firms in an international setting. Drawing upon theories on the 
#process and contexts of technology diffusion, we develop an integrative model to examine three assimilation stages: initiation -> adoption -> routinization. The model features technological, organizational, and environmental contexts as prominent antecedents of this three-stage assimilation process. Based on this model, we hypothesize how technology readiness, technology integration, firm size, global scope, managerial obstacles, competition intensity, and regulatory environment influence e-business assimilation at the firm level. A unique data set of 1,857 firms from 10 countries is used to test the conceptual model and hypotheses. To probe deeper into the influence of the environmental context, we compare two subsamples from developed and developing countries. Our empirical analysis leads to several key findings: (1) Competition positively affects initiation and adoption, but negatively impacts routinization, suggesting that too much competition is not necessarily good for technology assimilation because it drives firms to chase the latest technologies without learning how to use existing ones effectively. (2) Large firms tend to enjoy resource advantages at the initiation stage, but have to overcome structural inertia in later stages. (3) We also find that economic environments shape innovation assimilation: Regulatory environment plays a more important role in developing countries than in developed countries. Moreover, while technology readiness is the strongest factor facilitating assimilation in developing countries, technology integration turns out to be the strongest in developed countries, implying that as e-business evolves, the key determinant of its assimilation shifts from accumulation to integration of technologies. Together, these 
#findings offer insights into how innovation assimilation is influenced by contextual factors, and how the effects may vary across different stages and in different environments." keywords:"developed country,assimilation shift,latest technology,different countries,technology readiness,three-stage assimilation process,technology diffusion perspective,assimilation stage,innovation assimilation,environmental context,technology integration,technology assimilation,e business,competition,positive affect,developing country,conceptual model" n_citation:877


#16250677

#j_pacmpl_KissFEJ19 :Article mdate:"2021-02-17" name:"Higher-order type-level programming in Haskell." pages:"102:1-102:26" year:2019 
#volume:3 number:"ICFP" ee:"https://doi.org/10.1145/3341706" abstract:"Type family applications in Haskell must be fully saturated. This means that all type-level functions have to be first-order, leading to code that is both messy and longwinded. In this paper we detail an extension to GHC that removes this restriction. We augment Haskell’s existing type arrow, |->|, with an unmatchable arrow, | >|, that supports partial application of type families without compromising soundness. A soundness proof is provided. 
#We show how the techniques described can lead to substantial code-size reduction (circa 80%) in the type-level logic of commonly-used type-level libraries whilst simultaneously improving code quality and readability." keywords:"Data types and structures,Polymorphism,Reusability,Software and its engineering ? Functional languages" n_citation:4

#normal line

#77t_gte_TR_0174_12_91_165->f_Computer_science :fos

count = 0
# with open("milleDB.dump", encoding="utf8") as milldb_file:
#     for line in milldb_file:
#         if count == 1625067:
#             print(line)
#             break
#         count+=1

#line 70044256
#a_Hal_Tily->"MIT" :affiliation label:"former"

with open("milleDB.dump", encoding="utf8") as milldb_file:
    for line in milldb_file:
        print(line)
        if count > 100:
            break
        count+=1
