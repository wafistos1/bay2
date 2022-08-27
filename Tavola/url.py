

from bs4 import BeautifulSoup
import requests
import time
import pandas as pd


list_product_urls = [
    [
'https://www.tavolashop.com/sa-ar/cookware/stovetops/frying-saute-pans?p=', 2   
    ],
    [
'https://www.tavolashop.com/sa-ar/cookware/stovetops/cookware-sets?p=', 2
    ],
    [
 'https://www.tavolashop.com/sa-ar/cookware/stovetops/grill-pans-griddles?p=', 2    
    ],
    [
'https://www.tavolashop.com/sa-ar/cookware/stovetops/saucepans?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/cookware/stovetops/woks?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/cookware/stovetops/stock-pots-pasta-pots?p= ', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/cookware/stovetops/casseroles-braisers?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/cookware/stovetops/cookware-cleaners?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/cookware/stovetops/milk-pots-double-boilers?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/cookware/oven/ovenware?p=', 3
    ],
    [
    'https://www.tavolashop.com/sa-ar/cookware/oven/roasting-pans?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/cookware/specialty-cookware/pressure-cookers?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/cookware/specialty-cookware/fondue-sets-raclette-makers?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/cookware/specialty-cookware/microwave-cookware?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/cookware/specialty-cookware/steamers-poachers?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/cookware/specialty-cookware/tagines-paella-pans?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/appliances/essential-appliances/juicers?p=', 3
    ],
    [
    'https://www.tavolashop.com/sa-ar/appliances/essential-appliances/stand-mixers-attachments?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/appliances/essential-appliances/food-processors?p=', 2
    ],
    [   
    'https://www.tavolashop.com/sa-ar/appliances/essential-appliances/hand-blenders?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/appliances/essential-appliances/toasters?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/appliances/essential-appliances/instant-pot?p=', 2
    ],
    
    [
    'https://www.tavolashop.com/sa-ar/appliances/coffee-tea/coffee-makers-grinders?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/appliances/coffee-tea/electric-kettles?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/appliances/specialty-appliances/food-dehydrators?p=', 2
    ],
    [   
    'https://www.tavolashop.com/sa-ar/appliances/specialty-appliances/yogurt-cheese-makers?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/appliances/specialty-appliances/ice-cream-makers?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/appliances/specialty-appliances/cupcake-makers?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/appliances/specialty-appliances/raclettes?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/knives/kitchen-knives/knife-sets?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/knives/kitchen-knives/paring-peeling-knives?p=', 2
    ],
    [   
    'https://www.tavolashop.com/sa-ar/knives/kitchen-knives/utility-knives?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/knives/kitchen-knives/slicing-carving-knives?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/knives/kitchen-knives/cleavers-boning-knives?p=', 2
    ],
    
    [
    'https://www.tavolashop.com/sa-ar/knives/kitchen-knives/bread-knives?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/knives/kitchen-knives/steak-knives?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/knives/kitchen-knives/speciality-knives?p=', 2
    ],
    [   
    'https://www.tavolashop.com/sa-ar/knives/kitchen-knives/santoku-knives?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/knives/knife-accessories/knife-storage?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/knives/knife-accessories/knife-sharpeners?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/knives/knife-accessories/cutting-boards?p=', 3
    ],
    [
    'https://www.tavolashop.com/sa-ar/knives/knife-accessories/kitchen-shears-scissors?p=', 2
    ],
    
    [
    'https://www.tavolashop.com/sa-ar/kitchen-tools/essential-kitchen-utensils/utensil-sets?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/kitchen-tools/essential-kitchen-utensils/spatulas-turners?p=', 3
    ],
    [
    'https://www.tavolashop.com/sa-ar/kitchen-tools/essential-kitchen-utensils/spoons-ladles?p=', 2
    ],
    [   
    'https://www.tavolashop.com/sa-ar/kitchen-tools/essential-kitchen-utensils/whisks-brushes?p=?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/kitchen-tools/food-preparation-tools/mandolines-slicers?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/kitchen-tools/food-preparation-tools/spiralizers-corers?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/kitchen-tools/food-preparation-tools/graters-zesters?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/kitchen-tools/food-preparation-tools/peelers?p=', 2
    ],
    
    [
    'https://www.tavolashop.com/sa-ar/kitchen-tools/food-preparation-tools/choppers-presses?p=', 3
    ],
    [
    'https://www.tavolashop.com/sa-ar/kitchen-tools/food-preparation-tools/ricers-mashers?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/kitchen-tools/food-preparation-tools/colanders-strainers?p=', 3
    ],
    [   
    'https://www.tavolashop.com/sa-ar/kitchen-tools/food-preparation-tools/mixing-bowls?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/kitchen-tools/food-preparation-tools/measuring-cups-spoons-jars?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/kitchen-tools/food-preparation-tools/tongs-forks?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/kitchen-tools/food-preparation-tools/chopping-boards?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/kitchen-tools/essential-tools-gadgets/kitchen-scales?p=', 2
    ],
    
    [
    'https://www.tavolashop.com/sa-ar/kitchen-tools/essential-tools-gadgets/thermometers-timers?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/kitchen-tools/essential-tools-gadgets/can-jar-openers?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/kitchen-tools/speciality-tools/salad-tools?p=', 4
    ],
    [   
    'https://www.tavolashop.com/sa-ar/kitchen-tools/speciality-tools/garlic-herb-tools?p=', 3
    ],
    [
    'https://www.tavolashop.com/sa-ar/kitchen-tools/speciality-tools/fruit-citrus-tools?p=', 3
    ],
    [
    'https://www.tavolashop.com/sa-ar/kitchen-tools/speciality-tools/meat-poultry-tools?p=', 3
    ],

    [
    'https://www.tavolashop.com/sa-ar/kitchen-tools/speciality-tools/kitchen-textiles?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/kitchen-tools/speciality-tools/flour-tools?p=', 2
    ],
    
    [
    'https://www.tavolashop.com/sa-ar/kitchen-tools/speciality-tools/pizza-pasta-tools?p=', 3
    ],
    [
    'https://www.tavolashop.com/sa-ar/kitchen-tools/speciality-tools/grill-tools?p=', 3
    ],
    [
    'https://www.tavolashop.com/sa-ar/kitchen-tools/speciality-tools/chef-torches?p=', 2
    ],
    [   
    'https://www.tavolashop.com/sa-ar/kitchen-tools/speciality-tools/egg-tools?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/kitchen-tools/seasoning-oil/salt-pepper-mills?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/kitchen-tools/seasoning-oil/spice-shakers-nut-tools?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/kitchen-tools/seasoning-oil/oil-vinegar-dispensers?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/kitchen-tools/seasoning-oil/mortars-pestles?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/kitchen-tools/storage-organization/food-storage-jars-containers?p=', 3
    ],
    [
    'https://www.tavolashop.com/sa-ar/kitchen-tools/storage-organization/food-covers?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/kitchen-tools/storage-organization/bread-bins?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/kitchen-tools/storage-organization/utensil-holders?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/kitchen-tools/beverage-tools/water-filters-bottles?p=', 3
    ],
    [
    'https://www.tavolashop.com/sa-ar/kitchen-tools/beverage-tools/carbonated-drink-makers?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/kitchen-tools/beverage-tools/ice-cube-trays?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/bakeware/pans-moulds/cake-pans?p=', 3
    ],
    [
    'https://www.tavolashop.com/sa-ar/bakeware/pans-moulds/bundt-pans?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/bakeware/pans-moulds/springforms-cheesecake-pans?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/bakeware/pans-moulds/pizza-pie-tart-pans?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/bakeware/pans-moulds/bread-loaf-pans?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/bakeware/pans-moulds/cupcake-muffin-pans?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/bakeware/pans-moulds/multi-cavity-pans?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/bakeware/pans-moulds/mini-treat-pans?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/bakeware/pans-moulds/baking-pans-cookie-sheets?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/bakeware/pans-moulds/pancake-waffles-pans?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/bakeware/pans-moulds/bakeware-sets?p=', 2
    ],
    
    
    
    [
    'https://www.tavolashop.com/sa-ar/bakeware/baking-tools/baking-pastry-tools?p=', 3
    ],
    [
    'https://www.tavolashop.com/sa-ar/bakeware/baking-tools/baking-cups-wraps?p=', 2
    ],

    [
    'https://www.tavolashop.com/sa-ar/bakeware/baking-tools/weighing-measuring-tools?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/bakeware/baking-tools/cookie-cutters-accessories?p=', 6
    ],
    [
    'https://www.tavolashop.com/sa-ar/bakeware/baking-tools/cooling-racks?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/bakeware/baking-tools/rolling-pins-baking-mats?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/bakeware/baking-tools/baking-pastry-tools?p=',3
    ],
    
    
    [
    'https://www.tavolashop.com/sa-ar/bakeware/display-storage/cake-cupcake-stands?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/bakeware/display-storage/cake-cupcake-boxes?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/bakeware/display-storage/cookie-boxes?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/bakeware/display-storage/candy-boxes-wrappers?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/bakeware/display-storage/treat-bags-boxes?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/bakeware/display-storage/cake-carriers-storage?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/bakeware/occasions/halloween?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/bakeware/occasions/christmas?p=', 3
    ],
    [
    'https://www.tavolashop.com/sa-ar/bakeware/occasions/valentine?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/bakeware/occasions/weddings?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/bakeware/occasions/parties-birthdays?p=', 4
    ],
    [
    'https://www.tavolashop.com/sa-ar/bakeware/occasions/baby-shower?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/bakeware/occasions/easter?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/bakeware/occasions/mothers-day?p=', 3
    ],
    [
    'https://www.tavolashop.com/sa-ar/bakeware/occasions/eid-el-adha?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/bakeware/occasions/eid-el-fitr?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/bakeware/occasions/back-to-school?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/bakeware/occasions/football-fever?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/bakeware/occasions/ramadan?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/cake-decoration/tools-accessories/decorating-tips-accessories?p=', 3
    ],
    [
    'https://www.tavolashop.com/sa-ar/cake-decoration/tools-accessories/decorating-tools-turntables?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/cake-decoration/tools-accessories/piping-bags-couplers-covers?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/cake-decoration/tools-accessories/decorating-sets?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/cake-decoration/tools-accessories/fondant-gum-paste-tools?p=', 4
    ],
    [
    'https://www.tavolashop.com/sa-ar/cake-decoration/tools-accessories/sugar-flower-making-tools?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/cake-decoration/tools-accessories/cake-decorating-molds?p=', 3
    ],
    [
    'https://www.tavolashop.com/sa-ar/cake-decoration/tools-accessories/mats-boards-rollers?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/cake-decoration/tools-accessories/plungers-cutters?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/cake-decoration/tools-accessories/cake-boards-drums-dummies?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/edibles/edibles-ingredients/sprinkles?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/edibles/edibles-ingredients/food-colors?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/edibles/edibles-ingredients/cake-mixes?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/edibles/edibles-ingredients/flavourings?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/coffee-tea/coffee/french-press?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/coffee-tea/coffee/moka-pot?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/coffee-tea/coffee/syphon?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/coffee-tea/coffee/pour-over-v60?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/coffee-tea/coffee/coffee-machines?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/coffee-tea/coffee/coffee-grinders?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/coffee-tea/coffee/milk-frothers?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/tea-coffee/coffee/gooseneck-kettles?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/tea-coffee/coffee/coffee-spare-parts-accessories?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/tea-coffee/tea/tea-press?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/tea-coffee/tea/tea-pots?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/tea-coffee/tea/tea-infusers-strainers?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/tea-coffee/tea/kettles?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/coffee-tea/tea/tea-warmers?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/tea-coffee/coffee-tea-serveware/thermal-flasks?p=', 3
    ],
    [
    'https://www.tavolashop.com/sa-ar/tea-coffee/coffee-tea-serveware/teacups?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/tea-coffee/coffee-tea-serveware/espresso-cups?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/tea-coffee/coffee-tea-serveware/arabic-coffee-cups?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/tea-coffee/coffee-tea-serveware/glasses-mugs?p=', 3
    ],
    [
    'https://www.tavolashop.com/sa-ar/tea-coffee/coffee-tea-serveware/tea-sets?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/tea-coffee/coffee-tea-serveware/coffee-tea-spoons?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/tea-coffee/coffee-tea-serveware/sugar-bowls-honey-pots-creamers?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/tea-coffee/coffee-tea-serveware/travel-mugs?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/table-home/tableware/dinnerware?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/table-home/tableware/cutlery-sets?p=', 3
    ],
    [
    'https://www.tavolashop.com/sa-ar/table-home/tableware/serving-tools?p=', 4
    ],
    [
    'https://www.tavolashop.com/sa-ar/table-home/tableware/serveware?p=', 3
    ],
    [
    'https://www.tavolashop.com/sa-ar/table-home/tableware/drinkware?p=', 3
    ],
    [
    'https://www.tavolashop.com/sa-ar/table-home/tableware/table-accessories?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/table-home/tableware/placemats?p=', 3
    ],
    [
    'https://www.tavolashop.com/sa-ar/table-home/tableware/salt-pepper-shakers?p=', 3
    ],
    [
    'https://www.tavolashop.com/sa-ar/table-home/tableware/dinner-plates?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/table-home/tableware/side-plates?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/table-home/tableware/bowls?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/table-home/tableware/serving-bowls?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/table-home/tableware/dessert-plates-cake-stands?p=', 3
    ],
    [
    'https://www.tavolashop.com/sa-ar/table-home/tableware/trays?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/table-home/tableware/cheese-boards?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/table-home/tableware/baskets?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/table-home/tableware/tablecloths-napkins?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/table-home/outdoor-dining/bbq-grills?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/table-home/outdoor-dining/picnic-baskets?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/table-home/outdoor-dining/cooler-bags?p=', 3
    ],
    [
    'https://www.tavolashop.com/sa-ar/table-home/homeware/mirrors?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/table-home/homeware/personal-care?p=', 3
    ],
    [
    'https://www.tavolashop.com/sa-ar/table-home/homeware/floor-mats?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/table-home/homeware/waste-bins?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/table-home/homeware/dish-racks?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/table-home/homeware/soap-dispensers?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/table-home/homeware/cleaning-organisation?p=', 3
    ],
    [
    'https://www.tavolashop.com/sa-ar/table-home/homeware/bathroom-tools?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/table-home/homeware/sensor-mirrors?p=', 2
    ],
    [
    'https://www.tavolashop.com/sa-ar/on-the-go/travel-accessories/water-bottles?p=', 3
    ],
    [
    'https://www.tavolashop.com/sa-ar/on-the-go/travel-accessories/travel-mugs-jars-flasks?p=', 5
    ],
    [
    'https://www.tavolashop.com/sa-ar/on-the-go/travel-accessories/lunch-boxes?p=', 4
    ],
    [
    'https://www.tavolashop.com/sa-ar/on-the-go/travel-accessories/pocket-knives?p=', 2
    ],
   


]

def get_data(url):
#
    print('Url:', url)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    cookies = {'session': '134-8225175-0355220'}
    r = requests.get(url, headers=headers, cookies=cookies)
    soup = BeautifulSoup(r.content, "html.parser")
    time.sleep(1)
    products = soup.find_all('li', {'class': 'item last'})
    
    liens = [toto.find('a')['href']  for toto in products]
    print('Len products', len(liens))
    list_liens = []
    
    for t in liens:
        list_liens.append(t)
#     print('list_cat1', list_cat1)
    data = {
        'url':list_liens,
        }
    # df = pd.DataFrame(data)
#     print(df)
#         print('Href: ', t['href'])
#     print("Soup get_data")
    return soup, list_liens


def getnextpage(soup):
   
    #Check if next url exist else send None objects
    # Return URL or None
    
    page = soup.find('a', {'class': 'next i-next'})
    # print('Page', page)
    
    try:
        # if next url exist 
        url2 = str(page['href'])
        return url2
        # print('', url2)
    except:
        print('No Next')
        pass
    return url2 


# Extract new urls of Rugaib site from url categories

# url = 'https://rawae.com/search?subsubcategory=Accessories-box-Q3HaJ&page=1'
list_urls = []


def scrap_url_product(url1):
    
    
    
    cat1 = url1['cat1']
    cat2 = url1['cat2']
    cat3 = url1['cat3']
    url = url1['url']
    data = []
    print(cat1, cat2, cat3)
    while True:
        soup, urls_list = get_data(url)
        
        for toto in urls_list:

            # print(f'URL:', toto)
            data.append({
            'url':toto,
            'cat1': cat1,
            'cat2': cat2,
            'cat3': cat3,
            })

        try:
            url = getnextpage(soup)
#             print('Url dans le while', url)
        except:
            break
    # print(data)
    return data
    print( f'Scrape done .')



