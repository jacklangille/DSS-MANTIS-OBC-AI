true_color = """
//VERSION=3

function setup() {
  return {
    input: ["B04", "B03", "B02", "dataMask"],
    output: { bands: 4 }
  };
}

// Contrast enhance / highlight compress


const maxR = 3.0; // max reflectance

const midR = 0.13;
const sat = 1.3;
const gamma = 2.3;

// remove the minimum Rayleigh scattering (check the Himalayas)

const ray = { r: 0.013, g: 0.024, b: 0.041 };

function evaluatePixel(smp) {
  const rgbLin = satEnh(sAdj(smp.B04 - ray.r), sAdj(smp.B03 - ray.g), sAdj(smp.B02 - ray.b));
  return [sRGB(rgbLin[0]), sRGB(rgbLin[1]), sRGB(rgbLin[2]), smp.dataMask];
}

const sAdj = (a) => adjGamma(adj(a, midR, 1, maxR));

const gOff = 0.01;
const gOffPow = Math.pow(gOff, gamma);
const gOffRange = Math.pow(1 + gOff, gamma) - gOffPow;

const adjGamma = (b) => (Math.pow((b + gOff), gamma) - gOffPow) / gOffRange;

// Saturation enhancement

function satEnh(r, g, b) {
  const avgS = (r + g + b) / 3.0 * (1 - sat);
  return [clip(avgS + r * sat), clip(avgS + g * sat), clip(avgS + b * sat)];
}

const clip = (s) => s < 0 ? 0 : s > 1 ? 1 : s;

//contrast enhancement with highlight compression

function adj(a, tx, ty, maxC) {
  var ar = clip(a / maxC, 0, 1);
  return ar * (ar * (tx / maxC + ty - 1) - ty) / (ar * (2 * tx / maxC - 1) - tx / maxC);
}

const sRGB = (c) => c <= 0.0031308 ? (12.92 * c) : (1.055 * Math.pow(c, 0.41666666666) - 0.055);
"""
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