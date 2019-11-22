package main

import (
	"database/sql"
	"io/ioutil"
	"net/http"
	"net/url"
	"os"
	"strconv"
	"strings"
	"time"

	"github.com/mitchellh/go-ps"

	_ "github.com/mattn/go-sqlite3"
)

func gethttp(urls string, interval time.Duration) (string, string) { //get string by http from url
	if interval < 3 {
		return "", ""
	}
	time.Sleep(time.Second * interval)
	if 1 < len(strings.Split(urls, "?")) { //encode query
		r := strings.NewReplacer("%26", "&", "%3D", "=")
		urls = strings.Split(urls, "?")[0] + "?" + r.Replace(url.QueryEscape(strings.Split(urls, "?")[1]))
	}
	println(urls)
	req, _ := http.NewRequest("GET", urls, nil)
	req.Header.Set("User-Agent", "wrapper_for_NicoNicoAPI")
	client := new(http.Client)
	resp, err := client.Do(req)

	fname := resp.Header.Get("Content-Disposition")
	if 1 < len(strings.Split(fname, "filename=")) { //get downloading filename
		fname = strings.Split(strings.Split(fname, "filename=")[1], " ")[0]
	} else {
		fname = strconv.FormatInt(time.Now().Unix(), 10) //get Unix time
	}

	if err == nil {
		defer resp.Body.Close()
		byteArray, err := ioutil.ReadAll(resp.Body)
		if err == nil {
			return string(byteArray), fname
		}
	}
	return "", ""
}

func checkdup() int { //prevent duplication
	pidInfo, err := ps.FindProcess(os.Getpid())
	if err == nil {
		ls, err := ps.Processes()
		if err == nil {
			for i := 0; i < len(ls); i++ {
				if pidInfo.Executable() == ls[i].Executable() && pidInfo.Pid() != ls[i].Pid() {
					println("dup:", pidInfo.Executable())
					return 1
				}
			}
			println("Non_duplication")
			return 0
		}
	}
	return -1
}

func main() {
	for tm := time.Now().Unix(); time.Now().Unix()-tm < 10750; {

		if checkdup() != 0 {
			return
		}

		db, err := sql.Open("sqlite3", "flask.sqlite")
		if err == nil {
			defer db.Close()
			urls, sha256s, dates := make([]string, 0), make([]string, 0), make([]time.Time, 0)

			//read_SQL
			a, err := db.Query("select sha256,url,date from nicoapi")
			defer a.Close()
			if err == nil {
				for a.Next() {
					urls = append(urls, "")
					sha256s = append(sha256s, "")
					dates = append(dates, time.Now())
					a.Scan(&sha256s[len(sha256s)-1], &urls[len(urls)-1], &dates[len(dates)-1])
				}
			}

			//fetch_data
			for i := 0; i < len(urls); i++ {
				db.Exec("delete from nicoapi where url=? and sha256=?", urls[i], sha256s[i])
				text, fname := gethttp(urls[i], 3)
				os.MkdirAll("nicoapi/"+sha256s[i], 0777)
				err := os.Chmod("nicoapi/"+sha256s[i], 0777)
				if err == nil {
					fname = "nicoapi/" + sha256s[i] + "/" + fname
					fp, err := os.Create(fname)
					if err == nil {
						defer fp.Close()
						fp.Write(([]byte)(text))
					}
					os.Chmod(fname, 0777)
				}
			}

		}
		time.Sleep(time.Second * 5)
	}
	println("nicoapi.go->timeout")
}
