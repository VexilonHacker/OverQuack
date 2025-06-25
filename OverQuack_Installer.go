package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"path/filepath"
	"runtime"
	"strconv"
	"strings"
)

var (
	disclaimerMsg         = "Before you start: dont be a cyber-villain. If you break laws with this, that's on you — not me. Use it smart. Stay legal"
	circuitpython_version = "9.2.1"
	firmwaresDir          = "OverQuack_installation/firmwares"
	srcDir                = "OverQuack_src"

	picoModules   = []string{"Pico", "Pico W", "Pico2", "Pico2 W"}
	requiredFiles = []string{"boot.py", "code.py", "duckyinpython.py", "webapp.py", "wsgiserver.py", "config.json", "payload.oqs"}

	Colors = map[string]string{
		"RESET":          "\033[0m",
		"RED":            "\033[31m",
		"GREEN":          "\033[32m",
		"YELLOW":         "\033[33m",
		"BLUE":           "\033[34m",
		"BRIGHT_BLUE":    "\033[94m",
		"BRIGHT_MAGENTA": "\033[95m",
		"BRIGHT_CYAN":    "\033[96m",
		"GOLD":           "\033[38;2;255;215;0m",
	}
)

func printColor(text, color string, newline bool) {
	if newline {
		fmt.Printf("%s%s%s\n", color, text, Colors["RESET"])
	} else {
		fmt.Printf("%s%s%s", color, text, Colors["RESET"])
	}
}

func readOption(prompt string, max int) int {
	reader := bufio.NewReader(os.Stdin)
	for {
		printColor(prompt, Colors["BLUE"], false)
		input, err := reader.ReadString('\n')
		if err != nil {
			printColor(fmt.Sprintf("Error reading input: %v", err), Colors["RED"], true)
			continue
		}
		input = strings.TrimSpace(input)
		num, err := strconv.Atoi(input)
		if err != nil || num < 1 || num > max {
			printColor("Invalid option", Colors["RED"], true)
			continue
		}
		return num
	}
}

func readString(prompt string) string {
	reader := bufio.NewReader(os.Stdin)
	for {
		printColor(prompt, Colors["BRIGHT_BLUE"], false)
		input, err := reader.ReadString('\n')
		if err != nil || strings.TrimSpace(input) == "" {
			printColor("Input cannot be empty", Colors["RED"], true)
			continue
		}
		return strings.TrimSpace(input)
	}
}

func askMountPath(label string) string {
	for {
		path := readString(fmt.Sprintf("Enter the full path to your Pico's mounted drive (e.g., /run/media/USERNAME/%s): ", label))
		path = strings.TrimRight(path, "/")
		if _, err := os.Stat(path); err == nil {
			if strings.HasSuffix(path, label) {
				return path
			}
			printColor(fmt.Sprintf("Path must end with \"%s\"", label), Colors["RED"], true)
		} else {
			printColor(fmt.Sprintf("Error: %v", err), Colors["RED"], true)
		}
	}
}

func showMenu() int {
	printColor("Plug your Pico while holding BOOTSEL button for 3 seconds then release it", Colors["GREEN"], true)
	printColor("[Click Enter to continue]  ", Colors["BLUE"], false)
	fmt.Scanln()
	for i, module := range picoModules {
		printColor(fmt.Sprintf("\n%d) ", i+1), Colors["RED"], false)
		printColor(module, Colors["GOLD"], false)
	}
	fmt.Println()
	choice := readOption("Select your board: ", len(picoModules))
	printColor("Selected board: ", Colors["GREEN"], false)
	printColor(picoModules[choice-1], Colors["YELLOW"], true)
	printColor(disclaimerMsg, Colors["RED"], true)
	printColor("Pressing Enter means you agreed :] ", Colors["BRIGHT_MAGENTA"], false)
	fmt.Scanln()
	return choice - 1
}

func listFiles(path string) []string {
	entries, err := os.ReadDir(path)
	if err != nil {
		printColor(fmt.Sprintf("Error reading directory: %v", err), Colors["RED"], true)
		os.Exit(1)
	}
	var files []string
	for _, entry := range entries {
		if !entry.IsDir() {
			files = append(files, entry.Name())
		}
	}
	return files
}

func waitForRemount(module string) {
	printColor(fmt.Sprintf("%s is ejected.\nPlease remount it now.\nPress [Enter] once the device is mounted to continue...", module), Colors["YELLOW"], false)
	fmt.Scanln()
}

func checkDirs() {
	dirs := []string{
		"OverQuack_Client",
		"OverQuack_installation",
		"OverQuack_src",
		"OverQuack_installation/firmwares",
		"OverQuack_src/lib",
	}
	allOk := true
	for _, dir := range dirs {
		if info, err := os.Stat(dir); err != nil || !info.IsDir() {
			printColor(fmt.Sprintf(" - Missing or invalid directory: %s", dir), Colors["RED"], true)
			allOk = false
		} else {
			printColor(fmt.Sprintf(" + Found directory: %s", dir), Colors["GREEN"], true)
		}
	}
	fmt.Println()
	if allOk {
		printColor("+ All installation directories are present.\n", Colors["BRIGHT_CYAN"], true)
	} else {
		printColor("- Some installation directories are missing.", Colors["RED"], true)
		os.Exit(1)
	}
}

func copyFile(srcFile, dstDir string) {
	dst := filepath.Join(dstDir, filepath.Base(srcFile))
	src, err := os.Open(srcFile)
	if err != nil {
		printColor(fmt.Sprintf(" * Error: %v", err), Colors["RED"], true)
		os.Exit(1)
	}
	defer src.Close()

	dstFile, err := os.Create(dst)
	if err != nil {
		printColor(fmt.Sprintf(" * Error: %v", err), Colors["RED"], true)
		os.Exit(1)
	}
	defer dstFile.Close()

	if _, err := io.Copy(dstFile, src); err != nil {
		printColor(fmt.Sprintf(" * Error: %v", err), Colors["RED"], true)
		os.Exit(1)
	}
	printColor(fmt.Sprintf(" + Copied \"%s\" to \"%s\"", srcFile, dstDir), Colors["GREEN"], true)
}

func copyDir(src, dst string) {
	finalDst := filepath.Join(dst, filepath.Base(src))
	printColor(fmt.Sprintf(" + Copying \"%s\" to \"%s\"", src, finalDst), Colors["GREEN"], true)
	filepath.WalkDir(src, func(path string, d os.DirEntry, err error) error {
		if err != nil {
			return err
		}
		relPath, _ := filepath.Rel(src, path)
		destPath := filepath.Join(finalDst, relPath)
		if d.IsDir() {
			return os.MkdirAll(destPath, 0755)
		}
		return copySingleFile(path, destPath)
	})
}

func copySingleFile(src, dst string) error {
	in, err := os.Open(src)
	if err != nil {
		return err
	}
	defer in.Close()

	out, err := os.Create(dst)
	if err != nil {
		return err
	}
	defer out.Close()

	_, err = io.Copy(out, in)
	return err
}

func firmwareFilename(module, version string) string {
	return fmt.Sprintf("adafruit-circuitpython-raspberry_pi_%s-en_US-%s.uf2", module, version)
}

func checkRequiredFiles(src string, required []string) {
	for _, file := range required {
		if _, err := os.Stat(filepath.Join(src, file)); err != nil {
			printColor(fmt.Sprintf("Missing required file: %s", file), Colors["RED"], true)
			os.Exit(1)
		}
	}
}

func LinuxSetup() {
	checkDirs()
	selected := showMenu()
	mount := askMountPath("RPI-RP2")
	copyFile(filepath.Join(firmwaresDir, "flash_nuke.uf2"), mount)
	waitForRemount(picoModules[selected])

	mount = askMountPath("RPI-RP2")
	module := strings.ReplaceAll(strings.ToLower(strings.TrimSpace(picoModules[selected])), " ", "_")
	firmware := firmwareFilename(module, circuitpython_version)
	copyFile(filepath.Join(firmwaresDir, firmware), mount)

	waitForRemount(picoModules[selected])
	mount = askMountPath("CIRCUITPY")

	copyDir(filepath.Join(srcDir, "lib"), mount)

	checkRequiredFiles(srcDir, requiredFiles)

	for _, f := range requiredFiles {
		copyFile(filepath.Join(srcDir, f), mount)
	}

}

func main() {
	if runtime.GOOS == "linux" || strings.Contains(strings.ToLower(runtime.GOOS), "bsd") {
		LinuxSetup()
	}
}
