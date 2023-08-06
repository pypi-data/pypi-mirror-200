package main

import (
	"github.com/stretchr/testify/assert"
	neturl "net/url"
	"testing"
)

func TestBuildJson(t *testing.T)  {
	inpData := map[string]*neturl.URL{
		"http": &neturl.URL{
			Scheme: "http",
			Host:   "proxy.antizapret.prostovpn.org:3128",
		},
		"https": &neturl.URL{
			Scheme: "http",
			Host:   "proxy.antizapret.prostovpn.org:3128",
		},
	}

	expected := "{\"Proxy\":{\"http\":\"http://proxy.antizapret.prostovpn.org:3128\",\"https\":\"http://proxy.antizapret.prostovpn.org:3128\"},\"Error\":\"\"}"

	result := buildJson(inpData, nil)

	assert.Equal(t, expected, result)
}
