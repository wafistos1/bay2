
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import requests
import pandas as pd



list_urls = [
    {'cat1': 'المكياج', 'cat2': 'الوجه', 'cat3': 'البرايمر','url': 'https://aynma.com/makeup-face-primer/c970079703', 'page': 5},
    {'cat1': 'المكياج', 'cat2': 'الوجه', 'cat3': 'كريم الاساس - الفاونديشن','url': 'https://aynma.com/makeup-foundation/c1078186196', 'page': 30},
    {'cat1': 'المكياج', 'cat2': 'الوجه', 'cat3': 'بي بي و سي سي كريم','url': 'https://aynma.com/makeup-bb-cc-cream/c304676821', 'page': 6},
    {'cat1': 'المكياج', 'cat2': 'الوجه', 'cat3': 'خافي العيوب - الكونسيلر','url': 'https://aynma.com/makeup-concealer-corrector/c1878335190', 'page': 13},
    {'cat1': 'المكياج', 'cat2': 'الوجه', 'cat3': 'الباودر','url': 'https://aynma.com/makeup-powder/c1703181265', 'page': 16},
    {'cat1': 'المكياج', 'cat2': 'الوجه', 'cat3': 'الكونتور','url': 'https://aynma.com/makeup-contour/c121006881', 'page': 5},
    {'cat1': 'المكياج', 'cat2': 'الوجه', 'cat3': 'احمر الخدود - البلاشر','url': 'https://aynma.com/makeup-blusher/c197090512', 'page': 15},
    {'cat1': 'المكياج', 'cat2': 'الوجه', 'cat3': 'الإضاءة - الهايلايتر','url': 'https://aynma.com/makeup-highlighter/c1783960879', 'page': 13},
    {'cat1': 'المكياج', 'cat2': 'الوجه', 'cat3': 'مثبت المكياج','url': 'https://aynma.com/makeup-makeup-spray/c1144140840', 'page': 4},
    {'cat1': 'المكياج', 'cat2': 'الوجه', 'cat3': 'مزيل المكياج','url': 'https://aynma.com/makeup--makeup-removers/c371151657', 'page': 5},
    
    
    
    {'cat1': 'المكياج', 'cat2': 'العيون', 'cat3': 'ظلال العيون - الايشدو','url': 'https://aynma.com/makeup-eyeshadow/c1675915818', 'page': 26},
    {'cat1': 'المكياج', 'cat2': 'العيون', 'cat3': 'كحل - الايلاينر','url': 'https://aynma.com/makeup-eyeliner/c1036161323', 'page': 24},
    {'cat1': 'المكياج', 'cat2': 'العيون', 'cat3': 'الماسكرا','url': 'https://aynma.com/makeup-mascara/c1500831541?', 'page': 10},
    
    
    {'cat1': 'المكياج', 'cat2': 'الشفاة', 'cat3': 'احمر الشفاة - الأرواج','url': 'https://aynma.com/makeup-lipstick/c1461402672', 'page': 96},
    {'cat1': 'المكياج', 'cat2': 'الشفاة', 'cat3': 'محددات الشفاة','url': 'https://aynma.com/makeup-lip-liner/c754962454', 'page': 15},
    {'cat1': 'المكياج', 'cat2': 'الحواجب', 'cat3': '','url': 'https://aynma.com/makeup-eyebrow/c726793782', 'page': 17},
    {'cat1': 'المكياج', 'cat2': 'فرش وأدوات المكياج', 'cat3': '','url': 'https://aynma.com/makeup-brushes-tools/c1986441675', 'page': 18},
    
    
    {'cat1': 'العناية الشخصية', 'cat2': 'العناية بالوجه', 'cat3': '','url': 'https://aynma.com/personal-care-face/c1506016368', 'page': 5},
    {'cat1': 'العناية الشخصية', 'cat2': 'العناية بالجسم', 'cat3': 'https://aynma.com/personal-care-body/c1929742205','url': '', 'page': 5},
    {'cat1': 'العناية الشخصية', 'cat2': 'العناية بالفم', 'cat3': '','url': 'https://aynma.com/personal-care-oral/c1289922174', 'page': 5},
    {'cat1': 'العناية الشخصية', 'cat2': 'العناية باليدين و القدمين', 'cat3': '','url': 'https://aynma.com/personal-care-hand-foot/c516932991', 'page': 5},
    {'cat1': 'العناية الشخصية', 'cat2': 'العناية بالشعر', 'cat3': '','url': 'https://aynma.com/personal-care-hair/c980484985', 'page': 5},
    {'cat1': 'العناية الشخصية', 'cat2': 'العناية بالرجال', 'cat3': '','url': 'https://aynma.com/%D8%A7%D9%84%D8%B9%D9%86%D8%A7%D9%8A%D8%A9-%D8%A8%D8%A7%D9%84%D8%B1%D8%AC%D8%A7%D9%84/c831819298', 'page': 5},
    {'cat1': 'العناية الشخصية', 'cat2': 'العناية الصحية', 'cat3': '','url': 'https://aynma.com/%D8%A7%D9%84%D8%B9%D9%86%D8%A7%D9%8A%D8%A9-%D8%A7%D9%84%D8%B5%D8%AD%D9%8A%D8%A9/c57781539', 'page': 5},
    {'cat1': 'العناية الشخصية', 'cat2': 'واقي الشمس', 'cat3': '','url': 'https://aynma.com/sunscreen/c726366153', 'page': 5},



    {'cat1': 'العطور', 'cat2': 'عطورات رجالية', 'cat3': '','url': 'https://aynma.com/perfume-men-perfumes/c697355591'},
    {'cat1': 'العطور', 'cat2': 'عطورات نسائية', 'cat3': '','url': 'https://aynma.com/perfume-women-perfumes/c2071850048'},
    {'cat1': 'العطور', 'cat2': 'عطورات الشعر و الجسم', 'cat3': '','url': 'https://aynma.com/hair-body-perfumes/c1431964481'},
    {'cat1': 'العطور', 'cat2': 'البخور', 'cat3': '','url': 'https://aynma.com/%D8%A7%D9%84%D8%A8%D8%AE%D9%88%D8%B1/c656878146'},
 
    
    {'cat1': 'العدسات و النظارات', 'cat2': 'العدسات', 'cat3': 'عدسات لينس مي - LensMe','url': 'https://aynma.com/lens-me-lenses/c1804245043'},
    {'cat1': 'العدسات و النظارات', 'cat2': 'العدسات', 'cat3': 'عدسات ديفا - Diva','url': 'https://aynma.com/diva-lenses/c1163372348'},
    {'cat1': 'العدسات و النظارات', 'cat2': 'العدسات', 'cat3': 'عدسات انستازيا - Anesthesia','url': 'https://aynma.com/anesthesia-lenses/c1305414663'},
    {'cat1': 'العدسات و النظارات', 'cat2': 'العدسات', 'cat3': 'عدسات أخرى','url': 'https://aynma.com/other-lenses/c934179480'},
    {'cat1': 'العدسات و النظارات', 'cat2': 'العدسات', 'cat3': 'النظارات','url': 'https://aynma.com/sunglasses/c1211040536'},

    
    
    {'cat1': 'الاظافر', 'cat2': 'طلاء الاظافر', 'cat3': '','url': 'https://aynma.com/nails-polish/c1915836531'},
    {'cat1': 'الاظافر', 'cat2': 'العناية بالاظافر', 'cat3': '','url': 'https://aynma.com/nails-care/c434407037'},
    {'cat1': 'الاظافر', 'cat2': 'الاظافر الصناعية', 'cat3': '','url': 'https://aynma.com/nails-false/c1807852926'},
    
    {'cat1': 'منتجات الأطفال', 'cat2': 'مستلزمات الطعام', 'cat3': '','url': 'https://aynma.com/food-supplies/c684559941'},
    {'cat1': 'منتجات الأطفال', 'cat2': 'عربات الأطفال', 'cat3': '','url': 'https://aynma.com/baby-carriages/c2058005830'},
    {'cat1': 'منتجات الأطفال', 'cat2': 'أسرة و مقاعد الأطفال', 'cat3': '','url': 'https://aynma.com/baby-beds-seats/c1417137223'},
    {'cat1': 'منتجات الأطفال', 'cat2': 'الاستحمام والعناية بالبشرة', 'cat3': '','url': 'https://aynma.com/shower-skin-care/c643623744'},
    {'cat1': 'منتجات الأطفال', 'cat2': 'مناديل مبللة و حفاظات', 'cat3': '','url': 'https://aynma.com/wetwipes-diapers/c1882786369'},
   
    {'cat1': 'المنزل والمطبخ', 'cat2': 'الأجهزة المنزلية', 'cat3': '','url': 'https://aynma.com/home-appliances/c783560779'},
    {'cat1': 'المنزل والمطبخ', 'cat2': 'المطبخ وأدوات الطعام', 'cat3': '','url': 'https://aynma.com/kitchen-dining/c2022793044'},
    {'cat1': 'المنزل والمطبخ', 'cat2': 'معطرات المنزل', 'cat3': '','url': 'https://aynma.com/home-perfume/c1249803861'},
    {'cat1': 'المنزل والمطبخ', 'cat2': 'الحمامات', 'cat3': '','url': 'https://aynma.com/home-bath/c608476502'},

    {'cat1': 'الأجهزة', 'cat2': 'اجهزة تصفيف الشعر', 'cat3': '','url': 'https://aynma.com/hair-devices/c1106676902'},
    {'cat1': 'الأجهزة', 'cat2': 'اجهزة ازالة الشعر', 'cat3': '','url': 'https://aynma.com/hair-removal-devices/c1840827040'},

    {'cat1': 'اكسسوارات الجوال', 'cat2': 'الكابلات والوصلات', 'cat3': '','url': 'https://aynma.com/Cables/c1531910051'},
    {'cat1': 'اكسسوارات الجوال', 'cat2': 'سماعات الراس والأذن و مكبرات الصوت', 'cat3': '','url': 'https://aynma.com/speakers-headphones/c116479405'},
    {'cat1': 'اكسسوارات الجوال', 'cat2': 'الحافظات والأغطية', 'cat3': '','url': 'https://aynma.com/covers/c1356756142'},
    {'cat1': 'اكسسوارات الجوال', 'cat2': 'لاصقات حماية الشاشات', 'cat3': '','url': 'https://aynma.com/screen-protector/c581211055'},
    {'cat1': 'اكسسوارات الجوال', 'cat2': 'الاكسسوارات', 'cat3': '','url': 'https://aynma.com/phone-accessories-accessories/c2088874664'},
    {'cat1': 'اكسسوارات الجوال', 'cat2': 'شواحن الحائط', 'cat3': '','url': 'https://aynma.com/chargers-adapters/c1315885481'},
    {'cat1': 'اكسسوارات الجوال', 'cat2': 'الباور بانك', 'cat3': '','url': 'https://aynma.com/power-banks/c407629994'},

]

