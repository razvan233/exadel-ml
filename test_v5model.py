import spacy
from bs4 import BeautifulSoup
import requests
import csv
import re
import regex
import string
urls = [
    "https://www.factorybuys.com.au/products/euro-top-mattress-king",
    "https://dunlin.com.au/products/beadlight-cirrus",
    "https://themodern.net.au/products/hamar-plant-stand-ash",
    "https://furniturefetish.com.au/products/oslo-office-chair-white",
    "https://hemisphereliving.com.au/products/",
    "https://interiorsonline.com.au/products/interiors-online-gift-card",
    "https://livingedge.com.au/products/tables/dining",
    "https://www.knoll.com/design-plan/products/by-designer/knoll",
    "https://www.balirepublic.com.au/products/fabric-cleaner",
    "https://vastinterior.com.au/products/samson-daybed-single-2",
    "https://www.hudsonfurniture.com.au/products/string-weave-timber-stool",
    "https://dhfonline.com/products/gift-card",
    "https://www.tandemarbor.com/products/kaiser-box-bed-blush-plush-velvet",
    "https://www.perchfurniture.com/products/hoyt-chair",
    "https://4-chairs.com/products/mason-chair",
    "https://www.theinside.com/products/x-bench-onyx-austin-stripe-by-old-world-weavers/PTM_XBench_OnyxAustinStripeByOldWorldWeavers",
    "https://pinchdesign.com/products/yves-desk",
    "https://www.do-shop.com/products/gift-card",
    "https://claytongrayhome.com/products/palecek-coco-ruffle-mirror",
    "https://dfohome.com/products/patio-furniture/swings/all-swings",
    "https://www.kmpfurniture.com/fire_collection/products/beds_80.html",
    "https://www.furnitureworldgalleries.com/products/",
    "https://cityfurnitureshop.com/collections/greenington/products/azara-bed",
    "https://www.theguestroomfurniture.com/products/",
    "https://www.danishinspirations.com/products/products/bedroom/page/3/",
    "https://columbineshowroom.com/products/",
    "https://emfurn.com/products/aaron-sofa",
    "https://galvinbrothers.co.uk/products/alfandbud",
    "https://tyfinefurniture.com/products/enso-platform-bed",
    "https://24estyle.com/products/eliza-fan",
    "https://www.cranmorehome.com.au/products/gift-card",
    "https://www.vavoom.com.au/products/ebony-chest",
    "https://www.goodwoodfurniture.com.au/products/wardrobes/colonial-robe/",
    "https://valentinesfurniture.com.au/products/",
    "https://www.yellowleafhammocks.com/products/hammock-gift-card",
    "https://asplundstore.se/products/fish-bricka",
    "https://distinctive-interiors.com/products/",
    "https://www.comfortfurniture.com.sg/sale/products/office",
    "https://www.mybudgetfurniture.com/products/3pc-sectional",
    "https://www.fads.co.uk/products/living/sofas/sofa-beds/",
    "https://www.hipvan.com/products/sleep-mattress?ref=nav_dropdown",
    "https://dwell.co.uk/products/sleep/type/bed/",
    "https://www.timothyoulton.com/products/living/sectional-sofas",
    "https://www.warmnordic.com/global/products/news",
    "https://www.royaloakfurniture.co.uk/products/pop-bench",
    "https://mulamu.com/products/membership",
    "https://theodores.com/products/",
    "https://www.jensen-lewis.com/products/guardsman-gold-complete-plan",
    "https://cultdesign.co.nz/products/molloy-chair",
    "https://www.gloster.com/en/products/materials/teak",
    "https://capsulehome.com/products/frey-sofa'%3EFrey%20Sofa%3C/a%3E%20and%20I%20wanted%20to%20share%20it%20with%20you",
    "https://www.normann-copenhagen.com/en/en/products/tivoli/lamps/toli-lamp--20-cm-eu-5005028",
    "https://allwoodfurn.com/products/group-119-rustic-two-tone-gathering-table-and-barstools",
    "https://lostine.com/products/jack-chairs",
    "https://www.somedaydesigns.co.uk/products/muuto-tip-lamp?variant=513748041743",
    "https://www.mainecottage.com/collections/workspace/products/big-cay-desk",
    "https://www.antoninimodernliving.com/products/",
    "https://vancouverwoodworks.com/products/aamerica-wslcb5091",
    "https://www.kannoa.com/products/lipa-barstool",
    "https://furnitureoutletnc.com/products/deluxe-full-mattress",
    "https://www.thefurnituremegastore.co.uk/products/noir-80x180-cm-wall-mirror",
    "https://eurolivingfurniture.com/products/746-writing-desk",
    "https://www.efurnitureny.com/products/wardrobes-and-closets/wardrobe-closet-and-armoires",
    "https://decorium.us/products/costa-adjustable-barstool",
    "https://www.softsquare.com/collections/usm-haller/products/usm-haller-media-o1",
    "https://najarianfurniture.com/products/roma-sofa-pebble",
    "https://qualitywoods.com/products/qw-amish-mckee-6pc-dining-set?variant=31793708105810",
    "https://americanbackyard.com/products/gift-card",
    "https://www.roccityfurniture.com/products/abney-4pc-set/",
    "https://craftassociatesfurniture.com/products/craft-associates-wool-lounge-chairs-1519",
    "https://huset-shop.com/products/gift-card",
    "https://www.scotmeachamwoodhome.com/products/hodges-tweed",
    "https://www.espasso.com/products/tearsheet/1815",
    "https://sika-design.com/products/belladonna-nature",
    "https://www.dimshome.com/products/eave-desk",
    "https://thebellacottage.com/products/barrel-bar",
    "https://www.skandium.com/products/ch24-soft",
    "https://www.woodwaves.com/products/gray-floating-tv-stand-entertainment-center-eco-geo-lakewood",
    "https://jeremiahcollection.com/products/record-storage-console",
    "https://thefinestore.com/products/gift-card",
    "https://lorfords.com/collections/the-armchair-collection/products/the-bayswater-armchair",
    "https://pastperfect.sg/products/",
    "https://bastilleandsons.com.au/products/ottoman-leo",
    "https://classicwithatwist.com.au/products/1900-bench",
    "https://apato.com.au/products/work/kobo-st-desk/",
    "https://thewoodroom.com.au/products/take-me-back",
    "https://thebanyantree.com.au/products/gift-card",
    "https://ardoutdoor.com/products/",
    "https://hauserstores.com/products/mesa-sofa?view=product-alt",
    "https://boahaus.com/products/boahaus-urban-dressing-table",
    "https://tabularasa-furniture.com/collections/frontpage/products/ohmm-fiesta",
    "https://livingbydesign.net.au/products/sorensen-teak-bench-seat-dining",
    "https://www.living-home.co.uk/products/58-07-valencia-side-table",
    "https://relm.com.au/products/",
    "https://www.bellus.com/products/",
    "https://modernkomfort.ca/products/glen",
    "https://www.aarniooriginals.com/collections/shop/products/pony",
    "https://chansfurniture.com/products/copy-of-42-tennant-brand-modern-style-beatrice-bathroom-sink-vanity-tb-9433-v42-wenge-color",
    "https://hedgehousefurniture.com/products/windsor-bed",
    "https://shop.vanillawood.com/products/plume-wallpaper",
    "https://oakforless.com/products/gift-card",
    "https://www.castlery.com/products/spot-shelf",
    "https://homestreethome.ie/products/zinc-tray",
    "https://www.myconcept.com.hk/products/moo",
    "https://vauntdesign.com/products/forna-plant-stand-small",
    "https://asianteakfurniture.com/products/bali-teak-bench-atf388",
    "https://furnitica-vinova.myshopify.com/products/enim-donec-pede",
    "https://mikazahome.ca/products/page/4/",
    "https://barnabylane.com.au/products/spensley-tan",
    "https://www.modernfurniture.com.au/collections/on-sale/products/vision-suspended-sunbed",
    "https://teak-furniture-singapore.com/products/sweden-side-table",
    "https://teak-warehouse-sale.com/products/tws889lt-000-ta-lp",
    "https://www.countrysideamishfurniture.com/products/home-entertainment-centers/all/P40",
    "https://www.modishstore.com/products/twos-company-sunburst-antiqued-gold-wall-mirror",
    "https://loft-theme-demo-nashville.myshopify.com/products/black-chair",
    "https://teakco.com/products/amsterdam-2-drawer-bedside-table-tek168bs-002-ta",
    "https://big-sale-furniture.com/products/amsterdam-bench-150-x-35-be-150-35-ta",
    "https://taktcph.com/products/",
    "https://www.blackmango.com.au/products/gift-card",
    "https://candb.ca/products/10-gel-memory-foam-mattress",
    "https://www.oopenspace.com/products/nova-3",
    "https://thonet.co.nz/products/all",
    "https://www.dengiloutdoorfurniture.com/products/sofa-sets/rattan-sofa-sets/",
    "https://ubikhome.co.za/products/ada-tv-stand",
    "https://vintage-etc.com/products/tabeni-coat-stand",
    "https://www.hamac-shop.be/products/hamac-brasil-xxl-vert",
    "https://ikonitaly.com/products/minimaproject-chieut-table",
    "https://waltercox.co.uk/products/",
    "https://www.212concept.com/products/ikon-sofa",
    "https://vintagehomeboutique.ca/products/zinolin-teak-oil",
    "https://www.couchpotatocompany.com/collections/best-sellers/products/ro-armchair",
    "https://mueblesitaliano.ph/products/",
    "https://www.laura-james.co.uk/products/coffee-table-corona",
    "https://emesfurnishop.co.uk/products/ivo-wardrobe",
    "https://mossgardenhome.com/products/woodland-puzzle",
    "https://lesa.com.my/website2019/products/living/",
    "https://nyfurnitureoutlets.com/products/acme-furniture-versailles-classic-bed-king",
    "https://www.mydiscountmalta.com/products/mdm-wardrobe",
    "https://ifurnituresupply.com/products/spray-adhesive",
    "https://lazysusansusa.com/products/ls-16-myr-16-inches-in-diameter",
    "https://www.willowcreekteak.com/products/8pc-venice",
    "https://www.furnitureworldsaskatoon.com/products/",
    "https://hklivingusa.com/products/marble-terrazzo-board-multi-color",
    "https://scenicdecor.ca/products/grasshopper-storage-bin",
    "https://www.18karatstore.com/collections/new/products/argea",
    "https://mesasilla.ca/products/",
    "https://varkoa.com/products/sven-chair",
    "https://syscomseatings.com/products/workstation-manufacturers-bangalore/tile/",
    "https://www.insaraf.com/products/solid-wood-coasters",
    "https://www.nsquarestudio.com/products/odin-bedside-table",
    "https://lovenlight.eu/products/page/3/",
    "https://scanteak.com.sg/products/apen-bookcase",
    "https://www.finnavenue.com/products/carrara-round-dining-table",
    "https://singapore-furniture-sale.com/products/naples-teak-coffee-table-40x60x100-sfs638ct-000-ta",
    "https://1outdoorfurniture.com/products/asmund-outdoor-console-table-with-2-sink-set-1tf168inx-console-table-2-sink-set",
    "https://wholesaleclassicfurniture.com/products/lyon-french-victorian-lamp-table-bedside-timber-bedside-table-white-wcf168bs-101-pn-wh_1",
    "https://www.novena.com.sg/collections/stayhome-collection-for-immediate-delivery/products/altas-dining-set-solid-wood",
    "https://taylorbdesign.com/products/hb-1441",
    "https://houseofanli.com/products/gift-card",
    "https://hemma.sg/products/flower-planter?_pos=1&_sid=7be5737ba&_ss=r",
    "https://wholesaleteakcompany.com/collections/frontpage/products/sonoma-los-angeles-mirror-back-teak-glass-display-cabinet-wtc288dc-200-mr-pnm",
    "https://hmezsofa.sg/products/marble-tray",
    "https://www.vetrohome.com/products/dice-sofa",
    "https://gingerjarfurniture.com/products/page/3/",
    "https://solidaustin.com/products/cooks-sofa",
    "https://alteriors.ca/collections/herman-miller/products/nelson-saucer-bubble-lamp",
    "https://www.eurohausfurniture.com/products/novaluna-parigi-platform-bed",
    "https://www.ultimateliving.co.nz/products/adam",
    "https://www.rimufurniture.co.nz/products/riviera-1900-hutch-2/",
    "https://www.zavedo.nz/collections/wall-hooks/products/soho-hook-50",
    "https://www.jardin.co.nz/clearance/products/costa-chair-~-verbena/",
    "https://www.corcovado.co.nz/products/the-corcovado-kea-sofa",
    "https://www.lujo.co.nz/products/bean-bag-hook",
    "https://www.lujoliving.com/products/bean-bag-hook",
    "https://wrightsfurnitures.com/products/",
    "https://modernhomefurniture.com.au/products/albert-sofa",
    "https://www.konfoliving.com/products/miami-bean-bag-chair",
    "https://www.zipchair.com/products/stealth-recliner-with-boston-bruins-logo",
    "https://gousesfurniture.com/products/",
    "https://dkmodernfurniture.com/products/novah-desks?variant=20650194534470",
    "https://driftingwood.in/products/driftingwood-room-garden-love-folding-table-black",
    "https://jubileefurniturelv.com/products/anette-modern-leather-bed",
    "https://www.madebyhame.com/products/ladder",
    "https://interiorsinvogue.com/products/side-sofa-table-silver-finish-har189",
    "https://rileysrealwood.com/products/detail/magnistretch-12",
    "https://www.royalgarden.com/products/russel-4pc-seating-set",
    "https://centralcoastfurniture.com/collections/desks/products/lewis-desk",
    "https://www.henryandoliverco.com/products/gift-vouchers",
    "https://avehome.com/products/aria-desk",
    "https://elephanthead.co.uk/products/colourful-markers-cushion-cover",
    "https://www.coolstuffandaccessories.com/products/white-wood-dining-table",
    "https://french-classic-furniture.com/products/french-round-back-dining-chair-white-fcf688ch-000-rd-qa-wh_1",
    "https://habitekshop.com/products/model-5-oak",
    "https://plankandpipe.co.uk/products/copper-pipe-clothes-hanger-hooks",
    "https://www.polyteakoutdoor.com/products/polyteak-curved-outdoor-rocking-chair",
    "https://modholic.com/products/tulip-bar-table",
    "https://walkeredisonshop.com/products/jackson-slat-entry-table",
    "https://yoyo.co.nz/products/yoyo-gift-voucher",
    "https://newstartfurniture.com.au/products/4-four-poster-king-bed-frame",
    "https://panana.co.uk/products/3-seater-sofa-bed",
    "https://mahliainteriors.com.au/collections/mothers-day-15-off-sale/products/bone-inlay-floral-box-black",
    "https://choufani.com/products/primavera-bed",
    "https://copperbarnhome.com/products/gift-card",
    "https://www.ofo.com.au/products/hanging-pod-chair",
    "https://www.furniturecontracts.com.au/products/",
    "https://www.innerspace.net.au/products/STOOLS-5414",
    "https://americanwholesalefurniturewi.com/products/",
    "https://www.naturalgeo.com/products/natural-geo-jasmine-modern-wavy-abstract-gray-black-area-rug",
    "https://home-evolution.com/products/one-storys-not-enough/",
    "https://hamptonsstyle.com.au/products/hamptons-style-gift-card",
    "https://www.henkalab.com/products/kaona-table",
    "https://www.blockandchisel.co.za/products/special-features/promotion-53",
    "https://mintffe.com.au/products/",
    "https://modernityvintage.com/products/wilhelm-renz-metamorphic-coffee-table",
    "https://www.smallspaceplus.com/products/scube",
    "https://www.totemroad.com/products/gift-card",
    "https://whataroom.com/collections/new-arrival-rugs/products/arsene-r3475-aqu000",
    "https://penelopesgarden.us/products/cbd-starter-kit-save-5",
    "https://idsfurniture.com/categories/563349/simon/products/sim-s-ch/simon-side-chair",
    "https://www.byronbayhangingchairs.com.au/products/weekender",
    "https://www.homebarsusa.com/products/howard-miller-niagara-bar-693-001",
    "https://www.wellhunghammocks.com/products/mexican-hammock",
    "https://midcenturymasters.com/products/sculptural-ebonized-credenza-with-silver-leafed-front",
    "https://primrosehomeware.co.uk/products/pulley-clothes-airer-5-lath",
    "https://www.classic2modern.com/products/100-sofa",
    "https://www.mrandmrswhite.net/products/gift-card-2",
    "https://www.theteakplace.com.au/products/garden-bench-cushions",
    "https://www.mymoderndecor.com/sales@mymoderndecor.com/products/slim-bookcase-800923",
    "https://thecountryfurniture.com/products/sequoia",
    "https://lamporia.com/products/tbl4229a",
    "https://reecefurniture.com/products/jonkoping-sofa",
    "https://ulfertskids.com/products/rectangle-6",
    "https://www.thecurious.mx/collections/products/products/arcos-chair",
    "https://www.prestige-affairs.com/products/wishbone-y-chair",
    "https://vanspecial.com/products/self-planner",
    "https://www.wbjamieson.com/products/string-system",
    "https://www.canvasinteriors.com/collections/rugs/products/lia",
    "https://www.sunshinefurniture.com.au/products/albert-sofa",
    "https://elinahome.com/products/18-x-18-inch-satin-napkins-rhinestone-napkin-rings-party-supplies-christmas-decorations-wedding-birthday-baby-shower",
    "https://www.modernisedliving.com.au/products/3-sets-tank-pots-grey",
    "https://shop.humblecrew.com/products/lucky-theory-metal-chair",
    "https://www.simplyfurnishing.co.uk/products/4kids-1-door-desk-mobile-with-lemon-handles",
    "https://uniqwafurniture.com.au/collections/decorative-decor/products/bwindi-wall-art",
    "https://woodshopfogoisland.ca/products/bertha-chair",
    "https://profilesny.com/collections/art/products/bleach-scarf",
    "https://www.thefurniturefactory.org.uk/products/warwick-dining-set",
    "https://tiger-oak.com/products/skovby-portable-bar",
    "https://www.georgestreet.co.uk/products/e1-flush-3-light-ceiling-light/",
    "https://jordansinteriors.ca/products/park-slope-desk",
    "https://bestfurniture.co.nz/products/linea-sideboard",
    "https://www.imfurniturestore.com/products/sofa",
    "https://adona.in/products/adona-adonica-fusion-king-bed-plywood",
    "https://shop.gubi.com/products/epic-dining-table",
    "https://nativelifestyle.co.uk/products/cons-cesar01",
    "https://bohincstudio.com/collections/vases/products/jupiter-vase",
    "https://austinleathergallerytx.com/products/",
    "https://www.saladinostyle.com/products/nature",
    "https://finelinefurnitureandaccessories.com/products/colosso-woven-neoprene-hand-knotted-basket",
    "https://camerichseattle.com/products/rugs/",
    "https://domedeco.us/categories/639951/carpets/products/zu140200{slash}an/woolen-carpet-_singlequotes_zubair_singlequotes_",
    "https://donar.si/products/collodi",
    "https://www.gblfurniture.com/products/provence-1door-cabinet",
    "https://www.thechesterfieldshop.com/products/sofas/",
    "https://westbridgefurniturestoke.co.uk/products/view/890",
    "https://www.hopperstudio.com/products/sofia-nightstand",
    "https://www.angliarecliners.co.uk/products/swan/",
    "https://headandhaft.co.uk/products/tir",
    "https://hilaryandflo.co.uk/products/nice-print",
    "https://pepegarden.co.uk/products/erica-park-bench",
    "https://shannonsales.co.uk/products/special-offers/special-offers-and-sale-items/",
    "https://settlehome.co.uk/products/double-pair-of-triple-pinch-pleat-curtains-in-zoffany",
    "https://www.simplyhammocks.co.uk/collections/new-products/products/denim-hammock",
    "https://tiffanyjayne.co.uk/products/small-hooks",
    "https://thefurniture-house.co.uk/products/new-grey-recliner-sofa",
    "https://www.dillamores.co.uk/products/claremont-two-seater-sherborne/",
    "https://www.royalcraft.co.uk/products/ascot-shed-2",
    "https://www.fireandco.co.uk/products/fire",
    "https://www.askewsfurniture.co.uk/products/disposal-of-old-mattress",
    "https://www.bridgnorthfurniture.co.uk/products/verona-chair",
    "https://www.theurbaneditions.com/products/marston-wide-desk-on-minimalist-square-legs",
    "https://furniturevilla.co.uk/products/living-room-furniture/desk",
    "https://www.grandadsshedbrigg.co.uk/products/living/east-indies-living/",
    "https://hanchicsfurniture.co.uk/products/stag-f-b-sideboard",
    "https://limesinteriors.co.uk/collections/popular-items/products/abree-lamp",
    "https://www.nabisottomanfurniture.co.uk/products/chesterfield-diamante-bed-frame",
    "https://www.poppiesfurnituredirect.co.uk/apps/webstore/products/show/5373703",
    "https://thedorsetfurniturecompany.co.uk/products/arctic-white-high-gloss-150cm-shelf",
    "https://www.littletulip.com/products/set-200-marble-6",
    "https://urbansize.co.uk/products/hallway-tidy",
    "https://www.abowed.co.uk/products/oak-four-poster-bed",
    "https://www.oaktreeupholstery.co.uk/products/double-headboard-b-fabric",
    "https://shackletonsretail.co.uk/products/",
    "https://snugathome.co.uk/products/eiffel-dining-chair",
    "https://rusticland.co.uk/products/industrial-2x-handmade-x-dining-table-bench-frame-steel-large-table-pedestal-legs",
    "https://www.homeaffections.co.uk/products/wide-display-cabinet-540005-bonoca",
    "https://derwenthouseliving.co.uk/products/",
    "https://www.collectioni.com/products/noahs-ark-lounge-swivel-chair",
    "https://odafurniture.com/products/",
    "https://squarehome.com/products/",
    "https://thebeachfurniture.com.au/products/gift-card",
    "https://furnituremama.com/products/three-door-wardrobe-mirror-2",
    "https://gfurniture.ca/products/",

]


currency_pattern = re.compile(
    r'\b(?:\$|€|£|JPY|USD|EUR|GBP|INR|AUD|CAD|SGD|CNY|JPY)\b', re.IGNORECASE)
currency_pattern2 = regex.compile(
    r'(?:\p{Sc}|\b(?:USD|EUR|GBP|INR|AUD|CAD|SGD|CNY|JPY)\b)\s*\d+(?:,\d{3})*(?:\.\d+)?', re.IGNORECASE)
allowed_chars = set(string.ascii_letters + " .,;:-_/")

nlp = spacy.load('v5_product_ner_model')


def has_non_content_attribute(tag):
    for attribute in tag.attrs.values():
        if any(keyword in str(attribute).lower() for keyword in non_content_keywords):
            return True
    return False


products_with_url = []

try:
    with open('products_list_by_url_from_model_v5.csv', 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        for url in urls:
            res = requests.get(url)
            if res.status_code == 200:
                html_content = res.text
                soup = BeautifulSoup(html_content, 'html.parser')
                for script in soup(['script', 'style', 'nav', 'header', 'footer', 'form', 'img']):
                    script.extract()

                non_content_attributes = [
                    ('class', 'header'),
                    ('class', 'footer'),
                    ('class', 'nav'),
                    ('class', 'sidebar'),
                    ('data-section-id', 'sidebar'),
                    ('data-section-id', 'header'),
                    ('data-section-id', 'footer'),
                    ('data-section-id', 'nav'),
                    ('id', 'sidebar'),
                    ('id', 'header'),
                    ('id', 'footer'),
                    ('id', 'nav'),
                ]

                for attr, value in non_content_attributes:
                    for element in soup.find_all(attrs={attr: value}):
                        element.extract()
                non_content_keywords = [
                    'header', 'footer', 'nav', 'sidebar', 'advertisement', ]

                for tag in soup.find_all(has_non_content_attribute):
                    tag.extract()
                text = soup.get_text()
                text = ' '.join(text.split())

                doc = nlp(text)
                for ent in doc.ents:
                    product = ent.text
                    if currency_pattern.search(product) or currency_pattern2.search(product):
                        continue
                    if any(char not in allowed_chars for char in product):
                        continue
                    print(product)
                    if '.' in product:
                        product = product.split(".")[0]

                    products_with_url.append(
                        {'product': product.lower(), 'url': url})
        seen = set()
        new_products = []

        for product in products_with_url:
            identifier = tuple(product.items())
            if identifier not in seen:
                seen.add(identifier)
                new_products.append(product)

        for product_info in new_products:
            writer.writerow([product_info['url'], product_info['product']])

except Exception as err:
    print(err)
