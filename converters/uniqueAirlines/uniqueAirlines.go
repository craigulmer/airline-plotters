

package main

import (
	"fmt"
	"strings"
	//"bytes"
	//"sort"
	"os"
	"flag"
	"encoding/json"
	"io/ioutil"	
)

type PlaneRecord struct {
	id string
	points int64
	flight_list map[string] bool
	registration map[string] bool
	carrier_list map[string] bool
}
type PlaneRecordPtr *PlaneRecord

func NewPlaneRecord(id string) *PlaneRecord {
	return &PlaneRecord{
		id : id,
		flight_list  : make(map[string]bool),
		registration : make(map[string]bool),
		carrier_list : make(map[string]bool),
	}
}
func (pr *PlaneRecord) AddFlight(fid string){
	pr.flight_list[fid] = true;
	if len(fid) >= 2{
		pr.carrier_list[ fid[0:2] ] = true
	}
}
func (pr *PlaneRecord) AddRegistration(rid string){ pr.registration[rid] = true; }
func (pr *PlaneRecord) Dump(){
	fmt.Printf("%s\t%d\t%d\t%d\t num_carriers=%d\n",
		pr.id, pr.points, len(pr.flight_list), len(pr.registration), len(pr.carrier_list))
	
	for f:=range pr.carrier_list {
		fmt.Println(f)
	}
}
func JoinStringMap(src_map map[string]bool) string {
	a := make([]string,0,len(src_map))
	for k:=range src_map {
		a = append(a, k)
	}
	return strings.Join(a,"|")
}

func (pr *PlaneRecord) GetFlights() string {
	return JoinStringMap(pr.flight_list)
}
func (pr *PlaneRecord) GetRegistrations() string {
	return JoinStringMap(pr.registration)
}
func (pr *PlaneRecord) GetCarriers() string {
	return JoinStringMap(pr.carrier_list)
}


//func (pr *PlaneRecord) GetCarriers() string {
//	carrier_array := make([]string,0,len(pr.carrier_list))
//	for k:=range pr.carrier_list {
//		carrier_array = append(carrier_array, k)
//	}
//	return strings.Join(carrier_array,"|")
//}
func (pr *PlaneRecord) DumpBasic(){
	fmt.Printf("%s\t%d\t%d\t%s\t%s\t%s\n", pr.id, pr.points, len(pr.flight_list), pr.GetCarriers(), pr.GetFlights(), pr.GetRegistrations())
}




func main(){

	prec_ptrs:=make(map[string]*PlaneRecord)

	var dir = flag.String("dir", "../grab1", "Input Directory");
	flag.Parse();


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

				id := vals[0].(string)
				pptr := prec_ptrs[ id ]
				if pptr == nil {
					pptr = NewPlaneRecord(id)
					prec_ptrs[id] = pptr
				}

				pptr.points++
				pptr.AddFlight(vals[13].(string))
				pptr.AddRegistration(vals[9].(string))
				
			}
		}		
	}

	for _,val := range prec_ptrs {
		val.DumpBasic()
	}

	
	
}
