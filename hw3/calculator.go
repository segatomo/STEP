// A Go transliteration of
// https://github.com/xharaken/step2015/blob/master/calculator_modularize_2.py
// This is intended to keep the same shape and style of the
// @xharaken's original Python code, but please keep in mind that
// there are much more Go-friendly ways of writing much of this code.
// Consider watching Rob Pike's <r@google.com> talk on using Go to
// write a lexer (lexical scanner) here:
// https://talks.golang.org/2011/lex.slide recorded here
// https://www.youtube.com/watch?v=HxaD_trXwRE
package main

import (
	"bufio"
	"fmt"
	"go/token"
	"go/types"
	"log"
	"os"
	"unicode"
)

func main() {
	runTest()
	input := bufio.NewScanner(os.Stdin)
	for {
		fmt.Print("> ")
		if !input.Scan() || input.Text() == "" { // Reads a line from standard input.
			return // If it's empty, exit the program.
		}
		answer := Calculate(input.Text())
		fmt.Println("answer =", answer)
	}
}

func test(line string) {
	fmt.Printf("Test: %v\n", line)
	fset := token.NewFileSet()
	tokens := tokenize(line)
	tokens = preEvaluate(tokens)
	actualAnswer := evaluate(tokens)
	correctAns, err := types.Eval(fset, nil, token.NoPos, line)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("Actual answer: %#v\n", actualAnswer)
	fmt.Printf("Correct answer: %#v\n", correctAns.Value)
	fmt.Println("---------")

}

func runTest() {
	fmt.Println("==== Test started! ====")
	test("1")
	test("1.0")
	test("1+2")
	test("1-2")
	test("1*2")
	test("1/2")
	test("1.0+2.0")
	test("2.0-1.9")
	test("2.0*0.9")
	test("2.0/1.9")
	test("1.0+2.1-3")
	test("3*4/2+6/3-7*2")
	test("2+3.0*4/2+6/3-7*2")
	test("123+456*789-10/1112")
	test("10/9/8/7/6")
	test("2019*06/13")
	fmt.Println("==== Test finished! ===")
}

// Calculate turns a string like "1 + 3" into its corresponding
// numerical value (in this case 4).
func Calculate(line string) float64 {
	tokens := tokenize(line)
	tokens = prioritizeOperator(tokens)
	tokens = preEvaluate(tokens)
	return evaluate(tokens)
}

type customToken struct {
	// Specifies the type of the token. I'm using the word "kind" here
	// rather than "type" because type is a reserved word in Go.
	kind tokenKind

	// If kind is Number, then number is its corresponding numeric
	// value.
	number float64

	// 括弧の数
	bracket int

	// 優先順位
	priority int
}

// TokenKind describes a valid kinds of tokens. This acts kind of
// like an enum in C/C++.
type tokenKind int

// These are the valid kinds of tokens. Each gets automatically
// initialized with a unique value by setting the first one to iota
// like this. https://golang.org/ref/spec#Iota
const (
	Number tokenKind = iota
	Plus
	Minus
	Times
	Divide
)

func (k tokenKind) String() string {
	switch k {
	case Number:
		return "Number"
	case Plus:
		return "+"
	case Minus:
		return "-"
	case Times:
		return "*"
	case Divide:
		return "/"
	default:
		return "???"
	}
}

// Tokenize lexes a given line, breaking it down into its component
// tokens.
func tokenize(line string) []customToken {
	tokens := []customToken{customToken{Plus, 0, 0, 0}} // Start with a dummy '+' token
	index := 0
	num := 0
	cnt := 0
	for index < len(line) {
		var tok customToken
		switch {
		case unicode.IsDigit(rune(line[index])):
			tok, index = readNumber(line, index, num)
		case line[index] == '+':
			tok, index = readPlus(line, index, num)
		case line[index] == '-':
			tok, index = readMinus(line, index, num)
		case line[index] == '*':
			tok, index = readTimes(line, index, num)
		case line[index] == '/':
			tok, index = readDivide(line, index, num)
		case line[index] == '(':
			num++
			index++
			cnt++
			continue
		case line[index] == ')':
			num--
			index++
			continue
		default:
			log.Panicf("invalid character: '%c' at index=%v in %v", line[index], index, line)
		}
		tokens = append(tokens, tok)
	}
	// log.Printf("%#v", tokens)
	return tokens
}

// 優先順位をつける
func prioritizeOperator(tokens []customToken) []customToken {
	index := 0
	for index < len(tokens)-1 {
		if tokens[index].kind == Times || tokens[index].kind == Divide {
			tokens[index-1].priority++
			tokens[index].priority++
			tokens[index+1].priority++
		}
		index++
	}
	return tokens
}

// ゼロ除算を避ける
func isZero(i float64) bool {
	if i == 0 {
		return true
	}
	return false
}

// timesやdivideを先に計算し新しいtokenのリストを作る(3*4/2+6/3-7*2 -> 6+2-14 に変換)
func preEvaluate(tokens []customToken) []customToken {
	index := 0
	newTokens := []customToken{}
	// log.Printf("preEvaluate(%#v)", tokens)
	for index < len(tokens) {
		// log.Printf("for loop on index=%v token=%#v", index, tokens[index])
		switch tokens[index].kind {
		case Times:
			newTokens[len(newTokens)-1].number *= tokens[index+1].number
			index++
		case Divide:
			newTokens[len(newTokens)-1].number /= tokens[index+1].number
			index++
		default:
			newTokens = append(newTokens, tokens[index])
		}
		index++
	}
	return newTokens
}

// スライスからi番目の要素を削除する関数
func unset(tokens []customToken, i int) []customToken {
	if i >= len(tokens) {
		return tokens
	}
	return append(tokens[:i], tokens[i+1:]...)
}

// Evaluate computes the numeric value expressed by a series of
// tokens.
// 足し算引き算だけする
func evaluate(tokens []customToken) float64 {
	answer := float64(0)
	index := 0
	// log.Printf("evaluate(%#v)", tokens)
	for index < len(tokens) {
		// log.Printf("for loop on index=%v token=%#v", index, tokens[index])
		switch tokens[index].kind {
		case Number:
			switch tokens[index-1].kind {
			case Plus:
				answer += tokens[index].number
			case Minus:
				answer -= tokens[index].number
			// case Times:
			// 	answer *= tokens[index].number
			// case Divide:
			// 	if isZero(tokens[index].number) {
			// 		log.Panicf("")
			// 		os.Exit(1)
			// 	}
			// 	answer /= tokens[index].number
			default:
				log.Panicf("invalid syntax for tokens: %v", tokens)
			}
		}
		index++
	}
	return answer
}

func readPlus(line string, index int, num int) (customToken, int) {
	return customToken{Plus, 0, num, 0}, index + 1
}

func readMinus(line string, index int, num int) (customToken, int) {
	return customToken{Minus, 0, num, 0}, index + 1
}

func readTimes(line string, index int, num int) (customToken, int) {
	return customToken{Times, 0, num, 0}, index + 1
}

func readDivide(line string, index int, num int) (customToken, int) {
	return customToken{Divide, 0, num, 0}, index + 1
}

func readNumber(line string, index int, num int) (customToken, int) {
	number := float64(0)
	flag := false
	keta := float64(1)
DigitLoop:
	for index < len(line) {
		switch {
		case line[index] == '.':
			flag = true
		case unicode.IsDigit(rune(line[index])):
			number = number*10 + float64(line[index]-'0')
			if flag {
				keta *= 0.1
			}
		default:
			// "break DigitLoop" here means to break from the labeled for loop, rather than the switch statement. https://golang.org/ref/spec#Break_statements
			break DigitLoop
		}
		index++
	}
	return customToken{Number, number * keta, num, 0}, index
}
