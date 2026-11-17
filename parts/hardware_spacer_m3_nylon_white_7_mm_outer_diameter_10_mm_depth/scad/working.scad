// OOMP generic catalogue model; units: mm.
// Stud length is additional to body depth. Tapping depths are model assumptions.
variant = "full"; // [full, display]
family = "spacer";
connection_type = "plain";
depth_mm = 10;
stud_length_mm = 0;
tapped_depth_mm = 0;
bore_mm = 3.2;
outer_diameter_mm = 7;
across_flats_mm = 6;
thread_nominal_diameter_mm = 3;
thread_pitch_mm = 0.5;
edge_chamfer_mm = 0.12;
mouth_chamfer_mm = 0.2;
angular_segments = 96;
samples_per_pitch = 16;

// Boundary travels up the outside, then down any tapped/plain bore.
// Equal-height rings at shoulders form the annular shoulder faces.
n = angular_segments;
threaded = family == "standoff";
has_stud = connection_type == "stud_to_tapped" || connection_type == "stud_to_stud";
two_studs = connection_type == "stud_to_stud";
through = !threaded || connection_type == "tapped_to_tapped";
pitch = thread_pitch_mm;
diameter = threaded ? thread_nominal_diameter_mm : bore_mm;
minor = diameter - 5*sqrt(3)*pitch/8;
transition = mouth_chamfer_mm + (threaded ? 5*sqrt(3)*pitch/16 : 0);
tip_chamfer = mouth_chamfer_mm + 17*sqrt(3)*pitch/48;
function sorted(v) = len(v)<=1 ? v : let(p=v[0])
    concat(sorted([for(x=v) if(x<p-1e-8) x]), [p], sorted([for(x=v) if(x>p+1e-8) x]));
function reverse(v) = [for(i=[len(v)-1:-1:0]) v[i]];
function theta(i) = i*360/n;
function fract(x) = x-floor(x);
function phase_distance(i,z) = abs(fract(z/pitch-theta(i)/360+0.5)-0.5);
function thread_r(i,z) = minor/2 + min(5*sqrt(3)*pitch/16,
    max(0,(phase_distance(i,z)-0.125)*pitch*sqrt(3)));
function stud_r(i,z,tip) = min(diameter/2 - (variant=="full" ?
    min(17*sqrt(3)*pitch/48,max(0,(phase_distance(i,z)-0.0625)*pitch*sqrt(3))) : 0),
    diameter/2-tip_chamfer+abs(z-tip));
function body_r(i,z) = (threaded ? across_flats_mm/2/cos(theta(i)%60-30) : outer_diameter_mm/2)
    - max(0,edge_chamfer_mm-min(z,depth_mm-z));
function bore_r(i,z) = max(threaded ? (variant=="full" ? thread_r(i,z) : minor/2) : diameter/2,
    diameter/2+mouth_chamfer_mm-(through ? min(z,depth_mm-z) : depth_mm-z));
function stud_z(a,b,tip) = let(count=variant=="full" ? ceil(stud_length_mm/pitch*samples_per_pitch) : 1)
    sorted(concat([for(i=[0:count]) a+(b-a)*i/count], [tip==a ? tip+tip_chamfer : tip-tip_chamfer]));
body_z = sorted([0,edge_chamfer_mm,depth_mm-edge_chamfer_mm,depth_mm]);
low = through ? 0 : depth_mm-tapped_depth_mm;
count = threaded && variant=="full" ? ceil((depth_mm-low)/pitch*samples_per_pitch) : 1;
bore_z = two_studs ? [] : reverse(sorted(concat(
    [for(i=[0:count]) low+(depth_mm-low)*i/count],
    [depth_mm-mouth_chamfer_mm,depth_mm-transition],
    through ? [mouth_chamfer_mm,transition] : [])));
// Ring descriptors: [height, kind, tip]. Kind: 0 body, 1 stud, 2 bore.
rings = concat(
    has_stud ? [for(z=stud_z(-stud_length_mm,0,-stud_length_mm)) [z,1,-stud_length_mm]] : [],
    [for(z=body_z) [z,0,0]],
    two_studs ? [for(z=stud_z(depth_mm,depth_mm+stud_length_mm,depth_mm+stud_length_mm)) [z,1,depth_mm+stud_length_mm]] : [],
    [for(z=bore_z) [z,2,0]]);
function radius(i,ring) = ring[1]==0 ? body_r(i,ring[0]) :
    ring[1]==1 ? stud_r(i,ring[0],ring[2]) : bore_r(i,ring[0]);
points = concat([for(ring=rings) for(i=[0:n-1])
    [radius(i,ring)*cos(theta(i)),radius(i,ring)*sin(theta(i)),ring[0]]],
    through ? [] : [[0,0,rings[0][0]],[0,0,rings[len(rings)-1][0]]]);
center = len(rings)*n;
last = (len(rings)-1)*n;
// OpenSCAD winding is opposite to STL winding.
faces = concat(
    [for(j=[0:len(rings)-(through ? 1 : 2)]) for(i=[0:n-1]) each
        let(a=j*n+i,b=j*n+(i+1)%n,c=((j+1)%len(rings))*n+(i+1)%n,d=((j+1)%len(rings))*n+i)
        [[a,c,b],[a,d,c]]],
    through ? [] : [for(i=[0:n-1]) each let(k=(i+1)%n)
        [[center,i,k],[center+1,last+k,last+i]]]);
assert(family=="spacer" || family=="standoff");
assert(!threaded || connection_type=="tapped_to_tapped" || has_stud);
assert(depth_mm>0 && diameter>0 && pitch>0);
assert(variant=="full" || variant=="display");
assert(n>=24 && n%12==0 && samples_per_pitch>=8);
assert(mouth_chamfer_mm>0 && mouth_chamfer_mm<depth_mm/2);
assert(edge_chamfer_mm>=0 && edge_chamfer_mm<depth_mm/2);
assert(diameter+4*max(mouth_chamfer_mm,edge_chamfer_mm) < (threaded ? across_flats_mm : outer_diameter_mm));
assert(!has_stud || stud_length_mm>2*mouth_chamfer_mm);
assert(!through || !threaded || 2*transition<depth_mm);
assert(connection_type!="stud_to_tapped" || (tapped_depth_mm>transition && tapped_depth_mm<depth_mm));
color([0.86,0.85,0.81]) polyhedron(points=points,faces=faces,convexity=20);
