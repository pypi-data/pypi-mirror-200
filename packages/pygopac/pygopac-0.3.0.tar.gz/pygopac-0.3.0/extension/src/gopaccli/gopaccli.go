package main

import (
	"github.com/aleksey925/gopacparser"
	"encoding/json"
	"flag"
	"fmt"
	neturl "net/url"
	"os"
)

var pacFile = flag.String("pacFile", "", "Path to PAC file")
var url = flag.String("url", "", "URL of the requested site")

type Result struct {
	Proxy map[string]string
	Error string
}

func buildJson(proxy map[string]*neturl.URL, error error) string {
	errRes := ""
	if error != nil {
		errRes = error.Error()
	}

	result := &Result{}
	result.Error = errRes
	if len(proxy) != 0 {
		result.Proxy = map[string]string{
			"http":  proxy["http"].String(),
			"https": proxy["https"].String(),
		}
	} else {
		result.Proxy = map[string]string{}
	}

	resultJson, err := json.Marshal(result)
	if err != nil {
		return "marshal error"
	}
	return string(resultJson)
}

func initCliInterface() {
	flag.Parse()

	if *pacFile == "" && *url == "" {
		flag.PrintDefaults()
		os.Exit(1)
	}
}

func main() {
	initCliInterface()
	result, err := gopacparser.FindProxy(*pacFile, *url)
	fmt.Println(buildJson(result, err))
}
