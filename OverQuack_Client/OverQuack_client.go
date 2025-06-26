package main

import (
	"bufio"
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
	"os/exec"
	"path/filepath"
	"runtime"
	"strconv"
	"strings"
)

var (
	json_conf       = "config.json"
	bar             = "======================================"
	SUCCESS_CODE    = 0
	ERROR_CODE      = 1
	server_ip_addrs = ""
	ports           = []int{}
	dir             = "c2"
	Seperator       = ""
	url             = ""
	RESET           = "\033[0m"
	RED             = "\033[31m"
	GREEN           = "\033[32m"
	YELLOW          = "\033[33m"
	BLUE            = "\033[34m"
	BRIGHT_BLUE     = "\033[94m"
	BRIGHT_MAGENTA  = "\033[95m"
	BRIGHT_CYAN     = "\033[96m"
	GOLD            = "\033[38;2;255;215;0m"
	STEEL_BLUE      = "\033[38;2;70;130;180m"
	menu_ls         = []string{
		"List all files",
		"List all payloads",
		"Read content of a payload",
		"Upload a payload to PICO_W",
		"Delete a payload",
		"Run a payload",
		"Show ascii-art",
		"Exit",
	}
	max_number = len(menu_ls)
)

type APConfig struct {
	IPAddress string `json:"ip_address"`
	Ports     []int  `json:"ports"`
}

func PrintWithColors(data string, color string, newline int) {
	if newline == 1 {
		fmt.Printf("%s%s%s\n", color, data, RESET)
		return
	}
	fmt.Printf("%s%s%s", color, data, RESET)
}

func CreatURL(host string, dir string, ports_slice []int) string {
	for _, port := range ports_slice {
		url_t := fmt.Sprintf("http://%s:%d/%s", server_ip_addrs, port, dir)
		_, err := http.Get(url_t)
		if err != nil {
			continue
		} else {
			return url_t
		}
	}
	return "404"
}

func Ping(host string) bool {
	var cmd *exec.Cmd
	switch runtime.GOOS {
	case "windows":
		cmd = exec.Command("ping", "-n", "1", "-w", "1000", host)
	case "darwin":
		cmd = exec.Command("ping", "-c", "1", "-W", "1000", host)
	default: // linux or smth else
		cmd = exec.Command("ping", "-c", "1", "-W", "1", host)
	}

	_, err := cmd.CombinedOutput()
	if err == nil {
		return true
	} else {
		return false
	}
}

func SendPostRequest(url string, data string) string {
	resp, err := http.Post(url, "text/plain", bytes.NewBufferString(data))
	if err != nil {
		PrintWithColors(fmt.Sprintf("Request failed: %v", err), RED, 1)
		return "REQ_FAIL"
	}
	defer resp.Body.Close()

	// Read response
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		PrintWithColors(fmt.Sprintf("Failed to read response:  %v", err), RED, 1)
		return "READ_FAIL"
	}
	return string(body)
}

func BuildConnectionURL() {
	if Ping(server_ip_addrs) {
		PrintWithColors(fmt.Sprintf("%s is alive", server_ip_addrs), GREEN, 1)
	} else {
		PrintWithColors(fmt.Sprintf("%s is unreachable", server_ip_addrs), RED, 1)
		os.Exit(ERROR_CODE)
	}

	url = CreatURL(server_ip_addrs, dir, ports)
	if url == "404" {
		PrintWithColors(
			fmt.Sprintf("None of this ports: %v are open in %s", ports, server_ip_addrs),
			RED,
			1,
		)
		os.Exit(ERROR_CODE)
	}
	Seperator = SendPostRequest(url, "SEP")
}

func logo() {
	art := `
⠀⢀⣠⣤⣶⣶⣶⣤⣄⠀⠀⣀⣤⣶⣶⣶⣤⣄⡀⠀                                                                                 	⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⣤⣤⣤⣤⣀⣀
⠀⢸⣿⠁⠀⠀⠀⠀⠙⢷⡾⠋⠀⠀⠀⠀⠈⣿⡇                                                                                  	⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡤⠞⠋⠁⠀⠀⠀⠀⠀⠀⠉⠙⠲⣄⡀
⠀⠘⢿⡆⠀⠀⠀⠢⣄⣼⣧⣠⠔⠀⠀⠀⢰⡿⠃⠀                                                                                 	⠀⠀⠀⠀⠀⠀⠀⠀⡴⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣄
⠀⠀⠈⠻⣧⣤⣀⣤⣾⣿⣿⣷⣤⣀⣤⣼⠟⠁⠀⠀                                                                                 	⠀⠀⠀⠀⠀⠀⢀⡞⠁⣀⣀⣀⠀⠀⠀⠀⠀⣀⣠⣤⣤⣤⣤⣄⡀⠘⡆
⠀⠀⣰⡾⠋⠉⣩⣟⠁⠀⠀⠈⣻⣍⠉⠙⢷⣆⠀⠀     ⠀ ██████  ██    ██ ███████ ██████   ██████  ██    ██  █████   ██████ ██   ██	⠀⠀⠀⠀⢰⣿⣿⣿⣿⠉⠉⠉⣹⡆⠀⠀⣿⣿⣿⣿⡇⠀⢀⣀⡿⠀⢹
⠀⢀⣿⣀⣤⡾⠛⠛⠷⣶⣶⠾⠛⠛⢷⣤⣀⣿⡀⠀     ⠀██    ██ ██    ██ ██      ██   ██ ██    ██ ██    ██ ██   ██ ██      ██  ██ 	⠀⢀⣀⣠⡬⠿⠿⠟⠓⠚⠛⠉⠉⠉⠙⢲⡈⠉⠉⠉⠉⠉⠉⠀⠀⠀⢸⡆
⣰⡟⠉⣿⡏⠀⠀⠀⠀⢹⡏⠀⠀⠀⠀⢹⣿⠉⢻⣆     ⠀██    ██ ██    ██ █████   ██████  ██    ██ ██    ██ ███████ ██      █████  	⣞⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢳⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇
⣿⡇⠀⣿⣇⠀⠀⠀⣠⣿⣿⣄⠀⠀⠀⣸⣿⠀⢸⣿     ⠀██    ██  ██  ██  ██      ██   ██ ██ ▄▄ ██ ██    ██ ██   ██ ██      ██  ██ 	⠉⠓⠶⠶⣶⠶⠶⠶⠖⠒⠒⠒⠒⠒⢦⠀⣸⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇
⠙⣷⣼⠟⠻⣿⣿⡿⠋⠁⠈⠙⢿⣿⣿⠟⠻⣧⣾⠋     ⠀ ██████    ████   ███████ ██   ██  ██████   ██████  ██   ██  ██████ ██   ██	⠀⠀⠀⠀⠈⠓⠒⠶⠶⠶⠶⠶⡶⠶⠖⠚⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇
⠀⢸⣿⠀⠀⠈⢿⡇⠀⠀⠀⠀⢸⡿⠁⠀⠀⣿⡇⠀     ⠀                                                                           	⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⡇
⠀⠀⠻⣧⣀⣀⣸⣿⣶⣤⣤⣶⣿⣇⣀⣀⣼⠟⠀⠀     ⠀⠀                                                                          	⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣇
⠀⠀⠀⠈⠛⢿⣿⣿⡀⠀⠀⢀⣿⣿⡿⠛⠁⠀⠀⠀                                                                                 	⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣄
⠀⠀⠀⠀⠀⠀⠀⠙⠻⠿⠿⠟⠋⠀⠀⠀⠀⠀⠀                                                                                  	⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈

	`
	PrintWithColors(art, GOLD, 1)
}

func menu() {
	for index, elem := range menu_ls {
		fmt.Printf("%d) %s\n", index+1, elem)
	}
}

func InputString(msg string) string {
	reader := bufio.NewReader(os.Stdin)
	var option string

	for {
		PrintWithColors(msg, BRIGHT_BLUE, 0)
		line, err := reader.ReadString('\n')
		if err != nil {
			fmt.Println("Error reading input:", err)
			continue
		}

		option = strings.TrimSpace(line)
		if option == "" {
			fmt.Println("Input cannot be empty")
			continue
		}

		break
	}
	return option
}

func SelectedOption(max_number int) int {
	reader := bufio.NewReader(os.Stdin)
	var option int

	for {
		PrintWithColors("Enter option number: ", BLUE, 0)
		line, err := reader.ReadString('\n')
		if err != nil {
			PrintWithColors(fmt.Sprintf("Error reading input: %v", err), RED, 1)
			continue
		}

		line = strings.TrimSpace(line)
		option, err = strconv.Atoi(line)
		if err != nil {
			PrintWithColors("Invalid input", RED, 1)
			continue
		}
		if max_number < option {
			PrintWithColors("Invalid option", RED, 1)
			continue
		}

		break
	}
	return option
}

func Operation(opt int) {
	var data string
	switch opt {
	case 1:
		data = SendPostRequest(url, "LS")
	case 2:
		data = SendPostRequest(url, "PAYLOADS")
	case 3:
		payloadname := InputString("Enter PAYLOAD_NAME: ")
		command := fmt.Sprintf("READ%s%s", Seperator, payloadname)
		response := SendPostRequest(url, command)
		data = strings.TrimSpace(response)
	case 4:
		free_memory_str := SendPostRequest(url, "FREE_MEM")
		free_memory, err := strconv.Atoi(strings.TrimSpace(free_memory_str))
		if err != nil {
			PrintWithColors(fmt.Sprintf("Conversion error: %v", err), RED, 1)
			return
		}
		safe_memory := int(float64(free_memory) * 0.75) // use 75 % of free_memory to upload file
		PrintWithColors(
			fmt.Sprintf("Max File_Size that you can upload is %d KB", safe_memory/1000.0),
			YELLOW,
			1,
		)
		input := InputString("Enter filename path that you want to upload: ")
		if strings.HasPrefix(input, "~") {
			homeDir, err := os.UserHomeDir()
			if err == nil {
				input = filepath.Join(
					homeDir,
					strings.TrimPrefix(input, "~"),
				) // replace ~ with /home/$(whoami) for linxu users
			}
		}
		// Clean up relative paths (e.g., ../, ./)
		cleanedPath := filepath.Clean(input)
		// check if file exists
		fileInfo, err := os.Stat(cleanedPath)
		if err != nil || fileInfo.IsDir() {
			PrintWithColors(fmt.Sprintf("Error: Invalid file path: %v", err), RED, 1)
			return
		}
		// read file content
		content, err := os.ReadFile(cleanedPath)
		if err != nil {
			PrintWithColors(fmt.Sprintf("Error reading file: %v", err), RED, 1)
			return
		}
		if fileInfo.Size() > int64(safe_memory) {
			PrintWithColors(
				"File size is bigger than free memory in PICO_W, Cannot upload.",
				RED,
				1,
			)
			return
		}

		// extract just the filename (no path)
		fileNameOnly := filepath.Base(cleanedPath)
		if strings.HasPrefix(fileNameOnly, ".") {
			fileNameOnly = strings.TrimPrefix(fileNameOnly, ".")
		}

		PrintWithColors(fmt.Sprintf("Sending %s ...", fileNameOnly), YELLOW, 1)

		request := fmt.Sprintf("WRITE%s%s%s\n%s", Seperator, fileNameOnly, Seperator, content)
		data = SendPostRequest(url, request)

	case 5:
		payloadname := InputString("Enter PAYLOAD_NAME: ")
		request := fmt.Sprintf("DELETE%s%s", Seperator, payloadname)
		data = SendPostRequest(url, request)

	case 6:
		payloadname := InputString("Enter PAYLOAD_NAME: ")
		request := fmt.Sprintf("RUN%s%s", Seperator, payloadname)
		data = SendPostRequest(url, request)

	case 7:
		logo()
	case 8:
		PrintWithColors("Terminating Operation ->|^w^|->", GOLD, 1)
		os.Exit(SUCCESS_CODE)

	}
	if data != "" {
		data = fmt.Sprintf("%s\n%s\n%s", bar, data, bar)
		PrintWithColors(data, BRIGHT_CYAN, 1)
	}
}

func import_json() {
	data, err := os.ReadFile(json_conf)
	if err != nil {
		panic(err)
	}

	// Decode top-level into a map of raw JSON objects
	var root map[string]json.RawMessage
	if err := json.Unmarshal(data, &root); err != nil {
		panic(err)
	}

	var ap APConfig
	if err := json.Unmarshal(root["AP"], &ap); err != nil {
		panic(err)
	}

	server_ip_addrs = ap.IPAddress
	ports = ap.Ports
}

func main() {
	logo()
	import_json()
	BuildConnectionURL()
	PrintWithColors(fmt.Sprintf("url: %s, Sep: %s\n", url, Seperator), YELLOW, 1)
	for {
		menu()
		option := SelectedOption(max_number)
		Operation(option)

	}
}
