# These scripts specify which bands to download from Sentinel-2 imagery from sentinel Hub


#evalscript for an RGB satellite image from bands "B02", "B03", "B04"
# note: the 3.5 x multipliers on the return call brighten the image.
rgb = """
            //VERSION=3
            function setup() {
                return {
                    input: [{
                        bands: ["B02", "B03", "B04"]
                    }],
                    output: {
                        bands: 3
                    }
                };
            }
            function evaluatePixel(sample) {
                return [3.5*sample.B04, 3.5*sample.B03, 3.5*sample.B02];
            }
    """

#evalscript for an RGB and NIR satellite image from bands "B02", "B03", "B04", and"B08"
rgbnir = """
            //VERSION=3
            function setup() {
                return {
                    input: [{
                        bands: ["B02", "B03", "B04", "B08"]
                    }],
                    output: {
                        bands: 4
                    }
                };
            }
            function evaluatePixel(sample) {
                return [sample.B04, sample.B03, sample.B02, sample.B08];
            }
"""

# returns evalscript for a cloud mask overlaid onto the RGB image.
# Cloud masking is based on example 1.1 in this link: 
# https://sentinelhub-py.readthedocs.io/en/latest/examples/process_request.html
cloud_mask = """
        //VERSION=3
        function setup() {
            return {
                input: [{
                    bands: ["B02", "B03", "B04", "CLM"]
                }],
                output: {
                    bands: 3 
                }
            };
        }
        function evaluatePixel(sample) {
            if (sample.CLM == 1){
                return [0.75 + sample.B04, sample.B03, sample.B02]
            }
            return [3.5*sample.B04, 3.5*sample.B03, 3.5*sample.B02];
        }"""

# returns evalscript for the vegetation index, with pixel specification (B8-B4)/(B8+B4)
# B04 = red
# B08 = Infrared
ndvi = """
            //VERSION=3
            function setup() {
                return{
                    input: [{
                        bands: ["B04", "B08"]
                    }],
                    output: {
                        bands: 1,
                    }
                }
            }
            function evaluatePixel(sample) {
                let ndvi = (sample.B08 - sample.B04) / (sample.B08 + sample.B04)
                return [ ndvi ]
            }
        """

# returns evalscript for the chlorophyll index, with pixel specification (B8-B4)/(B8+B4)
# B04 = Red
# B05 = Red edge (in between red and NIR)
ndci = """
            //VERSION=3
            function setup() {
                return{
                    input: [{
                        bands: ["B04", "B05"]
                    }],
                    output: {
                        bands: 1,
                    }
                }
            }
            function evaluatePixel(sample) {
                let ndci = (sample.B05 - sample.B04) / (sample.B05 + sample.B04)
                return [ ndci ]
            }
        """
# Cyanobacteria Chlorophyll-a NDCI L1C
# Obtained from: https://custom-scripts.sentinel-hub.com/custom-scripts/sentinel-2/cyanobacteria_chla_ndci_l1c/
# Note: this uses many spectral bands that MANTIS will not have access to 
#(namely, aqua blue, and short wave infrared)
chla = """
        // CyanoLakes Chlorophyll-a L1C
        // Jeremy Kravitz & Mark Matthews (2020)

        // Water body detection - credit Mohor Gartner
        var MNDWI_threshold=0.42; //testing shows recommended 0.42 for Sentinel-2 and Landsat 8. For the scene in article [1] it was 0.8.
        var NDWI_threshold=0.4; //testing shows recommended 0.4 for Sentinel-2 and Landsat 8. For the scene in article [1] it was 0.5.
        var filter_UABS=true;
        var filter_SSI=false;
        function wbi(r,g,b,nir,swir1,swir2) {
            //water surface
            let ws=0;
            //try as it might fail for some pixel
            try {
                //calc indices
                //[4][5][1][8][2][3]
                var ndvi=(nir-r)/(nir+r),mndwi=(g-swir1)/(g+swir1),ndwi=(g-nir)/(g+nir),ndwi_leaves=(nir-swir1)/(nir+swir1),aweish=b+2.5*g-1.5*(nir+swir1)-0.25*swir2,aweinsh=4*(g-swir1)-(0.25*nir+2.75*swir1);
                //[10][11][12]
                var dbsi=((swir1-g)/(swir1+g))-ndvi,wii=Math.pow(nir,2)/r,wri=(g+r)/(nir+swir1),puwi=5.83*g-6.57*r-30.32*nir+2.25,uwi=(g-1.1*r-5.2*nir+0.4)/Math.abs(g-1.1*r-5.2*nir),usi=0.25*(g/r)-0.57*(nir/g)-0.83*(b/g)+1;
                //DEFINE WB
                if (mndwi>MNDWI_threshold||ndwi>NDWI_threshold||aweinsh>0.1879||aweish>0.1112||ndvi<-0.2||ndwi_leaves>1) {ws=1;}
                //filter urban areas [3] and bare soil [10]
                if (filter_UABS && ws==1) {
                    if ((aweinsh<=-0.03)||(dbsi>0)) {ws=0;}
                }
            }catch(err){ws=0;}
            return ws;
        }
        let water = wbi(B04,B03,B02,B08,B11,B12);

        // Floating vegetation
        function FAI (a,b,c) {return (b-a-(c-a)*(783-665)/(865-665))};
        let FAIv = FAI(B04,B07,B8A);

        // Chlorophyll-a
        function NDCI (a,b) {return (b-a)/(b+a)};
        let NDCIv = NDCI(B04,B05);
        let chl = 826.57 * NDCIv**3 - 176.43 * NDCIv**2 + 19 * NDCIv + 4.071; // From simulated data

        // Ture colour
        let trueColor = [3*B04,3*B03,3*B02];

        // Render colour map
        if (water==0) {
            return trueColor;
        } else if (FAIv>0.08){
            return [233/255,72/255,21/255];
        } else if (chl<0.5){
            return [0,0,1.0];
        } else if (chl<1){
            return [0,0,1.0];
        } else if (chl<2.5){
            return [0,59/255,1];
        } else if (chl<3.5){
            return [0,98/255,1];
        } else if (chl<5){
            return [15/255,113/255,141/255];
        } else if (chl<7){
            return [14/255,141/255,120/255];
        } else if (chl<8){
            return [13/255,141/255,103/255];
        } else if (chl<10){
            return [30/255,226/255,28/255];
    """
    
#Aquatic Plants and Algae Custom Script Detector
#Obtained from: https://custom-scripts.sentinel-hub.com/custom-scripts/sentinel-2/apa_script/
algae = """ 
//indices to apply a mask to water bodies
let moisture = (B8A-B11)/(B8A+B11);
let NDWI = (B03 - B08)/(B03 + B08);
let water_bodies = (NDWI-moisture)/(NDWI+moisture);

//indices to identify water plants and algae
let water_plants = (B05 - B04)/(B05 + B04);
let NIR2 = B04 + (B11 - B04)*((832,8 - 664,6)/(1613,7 - 664,6));
let FAI = B08 - NIR2;
//indices to apply a mask over clouds

//code taken from sentinel-2 custom scripts cby_cloud_detection by Peter Fogh

let bRatio = (B03 - 0.175) / (0.39 - 0.175);
let NDGR = index(B03, B04);
let gain = 2.5;
// natural color composition

let natural_color = [3*B04, 3*B03, 3*B02];
// cloud mask

function clip(a) {
    return Math.max(0, Math.min(1, a));
}

if (B11 > 0.1){
  if (bRatio > 1) { //cloud

    var v = 0.5*(bRatio - 1);
    return natural_color;
}
    else if (bRatio > 0 && NDGR>0) { 
        //cloud
        var v = 5 * Math.sqrt(bRatio * NDGR);
        return natural_color;
    }
}

//classify the presence of algae and water plants over water surfaces

if (NDWI < 0 && water_bodies > 0) return natural_color;
else return [FAI*8.5, water_plants*5.5, NDWI*1];
"""