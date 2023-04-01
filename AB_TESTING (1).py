#AB Testi ile BiddingYöntemlerinin Dönüşümünün Karşılaştırılması
#####################################################

# İş Problemi
#####################################################
# Facebook kısa süre önce mevcut "maximumbidding" adı verilen teklif verme türüne alternatif
# olarak yeni bir teklif türü olan "average bidding"’i tanıttı. Müşterilerimizden biri olanbombabomba.com,
# bu yeni özelliği test etmeye karar verdi veaveragebidding'in maximumbidding'den daha fazla dönüşüm
# getirip getirmediğini anlamak için bir A/B testi yapmak istiyor.A/B testi 1 aydır devam ediyor ve
# bombabomba.com şimdi sizden bu A/B testinin sonuçlarını analiz etmenizi bekliyor.Bombabomba.com için
# nihai başarı ölçütü Purchase'dır. Bu nedenle, istatistiksel testler için Purchasemetriğine odaklanılmalıdır.

#####################################################
# Veri Seti Hikayesi
#####################################################
# Bir firmanın web site bilgilerini içeren bu veri setinde kullanıcıların gördükleri ve tıkladıkları
# reklam sayıları gibi bilgilerin yanı sıra buradan gelen kazanç bilgileri yer almaktadır.Kontrol ve Test
# grubu olmak üzere iki ayrı veri seti vardır. Bu veri setleri ab_testing.xlsx excel’inin ayrı sayfalarında yer
# almaktadır. Kontrol grubuna Maximum Bidding, test grubuna AverageBidding uygulanmıştır.

# impression: Reklam görüntüleme sayısı
# Click: Görüntülenen reklama tıklama sayısı
# Purchase: Tıklanan reklamlar sonrası satın alınan ürün sayısı
# Earning: Satın alınan ürünler sonrası elde edilen kazanç

#####################################################
# Proje Görevleri
#####################################################

#####################################################
# Görev 1:  Veriyi Hazırlama ve Analiz Etme
#####################################################

# Adım 1:  ab_testing_data.xlsx adlı kontrol ve test grubu verilerinden oluşan veri setini okutunuz. Kontrol ve test grubu verilerini ayrı değişkenlere atayınız.

#kütüpahaneleri yükleyip dosyaları okutalım
import pandas as pd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import shapiro, levene, ttest_ind

pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

dataframe_control = pd.read_excel("pythonProject/WEEK4/ab_testing.xlsx" , sheet_name="Control Group")
dataframe_test = pd.read_excel("pythonProject/WEEK4/ab_testing.xlsx" , sheet_name="Test Group")

df_control = dataframe_control.copy()
df_test = dataframe_test.copy()

# Adım 2: Kontrol ve test grubu verilerini analiz ediniz.
#fonksiyon yazarak bakalım
def check_df(dataframe, head=5):
    print("##################### Shape #####################")
    print(dataframe.shape)
    print("##################### Types #####################")
    print(dataframe.dtypes)
    print("##################### Head #####################")
    print(dataframe.head())
    print("##################### Tail #####################")
    print(dataframe.tail())
    print("##################### NA #####################")
    print(dataframe.isnull().sum())
    print("##################### Quantiles #####################")
    print(dataframe.quantile([0, 0.05, 0.50, 0.95, 0.99, 1]).T)

check_df(df_control)
check_df(df_test)


# Adım 3: Analiz işleminden sonra concat metodunu kullanarak kontrol ve test grubu verilerini birleştiriniz.
df_control["group"] = "control"
df_test["group"] = "test"

df = pd.concat([df_control,df_test], axis=0,ignore_index=False)
df.head()
df.shape

df.groupby("group").agg({"Purchase": "mean"})

#####################################################
# Görev 2:  A/B Testinin Hipotezinin Tanımlanması
#####################################################
# Adım 1: Hipotezi tanımlayınız.

# H0 : M1 = M2 (Kontrol grubu ve test grubu satın alma ortalamaları arasında fark yoktur.)
# H1 : M1!= M2 (Kontrol grubu ve test grubu satın alma ortalamaları arasında fark vardır.)

# Adım 2: Kontrol ve test grubu için purchase(kazanç) ortalamalarını analiz ediniz

df.groupby("group").agg({"Purchase": "mean"})

#####################################################
# GÖREV 3: Hipotez Testinin Gerçekleştirilmesi
#####################################################

# Adım 1: Hipotez testi yapılmadan önce varsayım kontrollerini yapınız.Bunlar Normallik Varsayımı ve Varyans Homojenliğidir.

# Kontrol ve test grubunun normallik varsayımına uyup uymadığını Purchase değişkeni üzerinden ayrı ayrı test ediniz
# Normallik Varsayımı :
# H0: Normal dağılım varsayımı sağlanmaktadır.
# H1: Normal dağılım varsayımı sağlanmamaktadır
# p < 0.05 H0 RED
# p > 0.05 H0 REDDEDİLEMEZ
# Test sonucuna göre normallik varsayımı kontrol ve test grupları için sağlanıyor mu ?
# Elde edilen p-valuedeğerlerini yorumlayınız.


# Normal Dağılım: Ortalama ve medyan birbirine eşittir.
test_stat, pvalue = shapiro(df.loc[df["group"] == "control", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# p-value=0.5891
# HO reddedilemez. kontrol grubunun değerleri normal dağılım varsayımını sağlamaktadır.

test_stat, pvalue = shapiro(df.loc[df["group"] == "test", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

#####################################################

# Normal Dagılomı gözlemlemek adına görselleştirelim:

# Normal Dağılım: Ortalama ve medyan birbirine eşittir.

import seaborn as sns

# Histogram, nümerik değişkenlerin dağılımlarını görselleştirmede kullanılır.
# Tanımlanan grafik değişkenin histogram ve yoğunluğunu gösterir.
# Sadece histogramı görmek istersek kde parametresini False yapmamız yeterlidir.

def create_displot(dataframe, col):
    sns.displot(data=dataframe, x=col, kde=True)
    plt.show()

create_displot(df_control, "Purchase")

df_control["Purchase"].mean()
###################################################

test_stat, pvalue = shapiro(df.loc[df["group"] == "test", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))


# Her ikisinin de dagılımını gözlemlemek adına:
for group in list(df["group"].unique()):
    pvalue = shapiro(df.loc[df["group"] == group, "Purchase"])[1] #shapironun 1. indexteki degeri
    print(group,'p-value = %.4f' % pvalue)


# Varyans Homojenliği :

# grupların varyanslarının birbirine benzer olduğunu ifade eder.

# H0: Varyanslar homojendir.
# H1: Varyanslar homojen Değildir.
# p < 0.05 H0 RED
# p > 0.05 H0 REDDEDİLEMEZ
# Kontrol ve test grubu için varyans homojenliğinin sağlanıp sağlanmadığını Purchase değişkeni üzerinden test ediniz.
# Test sonucuna göre normallik varsayımı sağlanıyor mu? Elde edilen p-value değerlerini yorumlayınız.

test_stat, pvalue = levene(df.loc[df["group"] == "control", "Purchase"],
                           df.loc[df["group"] == "test", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# p-value=0.1083
# HO reddedilemez. Control ve Test grubunun değerleri varyans homejenliği varsayımını sağlamaktadır.
# Varyanslar Homojendir.


# Adım 2: Normallik Varsayımı ve VaryansHomojenliği sonuçlarına göre uygun testi seçiniz

# Varsayımlar sağlandığı için bağımsız iki örneklem t testi (parametrik test) yapılmaktadır.
# H0: M1 = M2 (Kontrol grubu ve test grubu satın alma ortalamaları arasında ist. ol.anl.fark yoktur.)
# H1: M1 != M2 (Kontrol grubu ve test grubu satın alma ortalamaları arasında ist. ol.anl.fark vardır)
# p<0.05 HO RED , p>0.05 HO REDDEDİLEMEZ

test_stat, pvalue = ttest_ind(df.loc[df["group"] == "control", "Purchase"],
                              df.loc[df["group"] == "test", "Purchase"],
                              equal_var=True) # Varyans homojemligi saglanmıyor olsaydı equal_var = False Weltch testini yapmasını saglar.

print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# Adım 3: Test sonucunda elde edilen p_valuedeğerini göz önünde bulundurarak kontrol ve test grubu satın alma
# ortalamaları arasında istatistiki olarak anlamlı bir fark olup olmadığını yorumlayınız.

# p-value=0.3493

# HO reddedilemez. Kontrol ve test grubu satın alma ortalamaları arasında istatistiksel olarak anlamlı farklılık yoktur.

##############################################################
# GÖREV 4 : Sonuçların Analizi
##############################################################

# Adım 1: Hangi testi kullandınız, sebeplerini belirtiniz.
#CEVAP:
#Verilerin normal dağılıma sahip olup olmadığını belirlemek için Normallik Varsayımı için shapiro testini kullandım.
#Belirlemek için Varyans Homojenliği için levene testi kullandım
#purchase_control/ test gruplarının varyanslarının eşit olup olmadığı.
#Tüm p_ değerleri 0.05'in üzerinde olduktan sonra t-testi (parametrik) kullandım.

# Adım 2: Elde ettiğiniz test sonuçlarına göre müşteriye tavsiyede bulununuz.
#CEVAP:
#Test sonuçlarına göre "maximumbidding" adı verilen teklif verme türü ile "average bidding" 'in getirdiği ortalama kazançlar arasında istatistiki
#olarak anlamlı bir farklılık yoktur.
#Ortalama teklif verme yönteminin tesadüfen daha fazla gösterim, satın alma ve kazanç sağladığı görülüyor.
#Bir süre daha gözlem yapılarak ve veri sayısı arttırılarak daha büyük bir örneklem kütlesi ile aynı testler tekrarlanabilir.

