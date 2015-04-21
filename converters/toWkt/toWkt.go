// toWkt: simple program to parse fr24 json data and convert to simple wkt format

package main

import (
	"fmt"
	"bytes"
	"sort"
	"os"
	"flag"
	"encoding/json"
	"io/ioutil"	
)


type marker struct {
	ts  int64    //10
	lat float64  //1
	lon float64  //2
   alt int      //4
}
type Markers []*marker

func (m Markers) Dump(id int) {
	for _,o := range m {
		fmt.Printf("%d\t%d\t%f\t%f\t%d\n", id, o.ts, o.lat, o.lon, o.alt);
	}
}
func (m Markers) ToWKT() string {
	var buffer bytes.Buffer
	buffer.WriteString("LINESTRING (");
	is_first := true;
	for _,o := range m {
		if(!is_first){
			buffer.WriteString(", ");
		} else {
			is_first = false;
		}
		s := fmt.Sprintf("%f %f %d %d", o.lon, o.lat, o.alt, o.ts);
		buffer.WriteString(s);
		//buffer.WriteString(o.lon+" "+o.lat+" "+o.alt+" ",o.ts);
		//fmt.Printf("%d\t%d\t%f\t%f\t%d\n", id, o.ts, o.lat, o.lon, o.alt);
	}
	buffer.WriteString(")");
	return buffer.String();
}


func (m Markers) Len() int { return len(m) }
func (m Markers) Swap(i,j int) { m[i],m[j] = m[j],m[i] }

type byTime struct{ Markers }
func (m byTime) Less(i,j int) bool { return m.Markers[i].ts < m.Markers[j].ts }


func main(){

	var mm map[string]Markers;
	mm=make(map[string]Markers);

	var dir = flag.String("dir", "../grab1", "Input Directory");
	flag.Parse();
	//fmt.Println("Input Directory: "+*dir);

	var srcdst map[string]string;
	srcdst=make(map[string]string);

	//dir:="../grab1";

	files,_ := ioutil.ReadDir(*dir)
	for _,f := range files {
		//if idx >2 { break; }

		//fmt.Println(f.Name());
		fi, err := os.Open(*dir+"/"+f.Name());
		if err != nil { panic(err) }
		defer func(){
			if err := fi.Close(); err != nil {
				panic(err)
			}
		}()
		
		dec := json.NewDecoder(fi);
		for {
			var entries map[string]interface{} 
			if err:= dec.Decode(&entries); err != nil { break } // panic(err) }
			
			for ref := range entries {
				if ref == "full_count" { continue }
				if ref == "version"    { continue }

				//fmt.Println(f.Name()+" "+ref);
				vals:=entries[ref].([]interface{})

				// Values:
				//  0 : registration (A9EC06)
            //  1 : lat
            //  2 : lon
            //  3 : Track (degrees)
            //  4 : altitude (ft)
            //  5 : speed (kt?)
            //  6 : ? "0000"
            //  7 : Radar station
            //  8 : aircraft type (B753)
            //  9 : registration (N73860)
            // 10 : Last heard time
            // 11 : Source airport (IAD)
            // 12 : Dest airport (SFO)
            // 13 : Airline code (UA1431)
            // 14 : ? 0
            // 15 : ? 0 Vertical speed?
            // 16 : Airlinecode (UAL1431)
            // 17 : Estimated arrival time




				new_marker := marker{}
				new_marker.ts = int64(vals[10].(float64)); 
				new_marker.lat = vals[1].(float64);
				new_marker.lon = vals[2].(float64);
				new_marker.alt = int(vals[4].(float64));

				//src := vals[11].(string);
				//dst := vals[12].(string);
				registration := vals[9].(string);
				airline := vals[13].(string);
				

				//flabel := vals[16].(string);
				flabel := vals[0].(string);
				marker_array := mm[ flabel ]; //ref
				mm[ flabel ] = append(marker_array, &new_marker);

				//srcdst[ flabel] = "\""+registration+"\"\t\""+airline+"\"\t"+src + "\t" + dst;
				srcdst[ flabel] = registration+"|"+airline;
			}
		}		
	}

	var id int;
	//Sort every entry's vals by time
	for k,v := range mm {
		//fmt.Println("#\t",id,"\tFLIGHT\t",k,"\t",srcdst[k] )
		sort.Sort(byTime{v})
		wkt:=v.ToWKT();
		//v.Dump(id)
		fmt.Printf("%d\t%s|%s\t%s\n",len(v), k,srcdst[k],wkt);
		//fmt.Println(k+"-"+srcdst[k]+"|"+len(v)+"\t"+wkt);
		id++;
	}


	

}
