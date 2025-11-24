from number_factorer.Factor_Number import (
    Number_Factorer,
    IncrementOrder,
    BabyGiantOrder,
    ShorFactorization,
    EkeraFactorization,
    ShorOrder,
    BeauregardOrder
)

nf = Number_Factorer(EkeraFactorization(), ShorOrder())

print(nf.factor(44))

