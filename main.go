package main

import (
	"flag"
	"os"

	"github.com/hanksudo/bot-currency/backup"
	"github.com/hanksudo/bot-currency/currency"
	"github.com/hanksudo/bot-currency/web"
	"github.com/robfig/cron/v3"
)

// RootPath - root of project
var RootPath string

func main() {
	RootPath, _ = os.Getwd()
	webPtr := flag.Bool("web", false, "Start web server")
	renewPtr := flag.Bool("renew", false, "Renew currency data")
	backupPtr := flag.Bool("backup", false, "Backup to Dropbox")
	flag.Parse()

	if len(os.Args) == 1 {
		flag.PrintDefaults()
	} else if *webPtr {
		c := cron.New()
		// Renew - Every one hour on weekday
		c.AddFunc("0 0 * * * 1,2,3,4,5", currency.Renew)
		// Backup - Every 3 hours on weekday
		c.AddFunc("0 0 */3 * * 1,2,3,4,5", backup.Start)
		c.Start()

		web.Start()
	} else if *renewPtr {
		currency.Renew()
	} else if *backupPtr {
		backup.Start()
	}
}
