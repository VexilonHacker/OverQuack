require.config({
  paths: {
    vs: 'https://cdn.jsdelivr.net/npm/monaco-editor@0.44.0/min/vs',
    'monaco-vim':
      'https://cdn.jsdelivr.net/npm/monaco-vim@0.4.2/dist/monaco-vim',
  },
});

define('vs/editor/common/commands/shiftCommand', [], function () {
  return {};
});

require(['vs/editor/editor.main', 'monaco-vim'], function (
  monacoInstance,
  MonacoVim,
) {
  window.monaco = monacoInstance;
  const unusedDecorations = new WeakMap();

  function dedent(str) {
    const lines = str.split('\n');
    let minIndent = Infinity;
    for (const line of lines) {
      if (line.trim().length === 0) continue;
      const match = line.match(/^(\s*)/);
      const indent = match ? match[1].length : 0;
      if (indent < minIndent) minIndent = indent;
    }
    if (minIndent === Infinity || minIndent === 0) return str;
    return lines.map((line) => line.slice(minIndent)).join('\n');
  }
  const holdKeys = [
    'CTRL',
    'CONTROL',
    'RCTRL',
    'RIGHT_CONTROL',
    'ALT',
    'OPTION',
    'RALT',
    'RIGHT_ALT',
    'ROPTION',
    'SHIFT',
    'RSHIFT',
    'RIGHT_SHIFT',
    'GUI',
    'WINDOWS',
    'COMMAND',
    'RGUI',
    'RWINDOWS',
    'RCOMMAND',
    'RIGHT_GUI',
    'ENTER',
    'TAB',
    'SPACE',
    'BACKSPACE',
    'ESC',
    'ESCAPE',
    'DELETE',
    'HOME',
    'END',
    'INSERT',
    'PAGEUP',
    'PAGEDOWN',
    'UPARROW',
    'DOWNARROW',
    'LEFTARROW',
    'RIGHTARROW',
    'UP',
    'DOWN',
    'LEFT',
    'RIGHT',
    'CAPSLOCK',
    'NUMLOCK',
    'SCROLLLOCK',
    'F1',
    'F2',
    'F3',
    'F4',
    'F5',
    'F6',
    'F7',
    'F8',
    'F9',
    'F10',
    'F11',
    'F12',
    'F13',
    'F14',
    'F15',
    'F16',
    'F17',
    'F18',
    'F19',
    'F20',
    'F21',
    'F22',
    'F23',
    'F24',
    'APP',
    'MENU',
    'PRINTSCREEN',
    'PAUSE',
    'BREAK',
    'A',
    'B',
    'C',
    'D',
    'E',
    'F',
    'G',
    'H',
    'I',
    'J',
    'K',
    'L',
    'M',
    'N',
    'O',
    'P',
    'Q',
    'R',
    'S',
    'T',
    'U',
    'V',
    'W',
    'X',
    'Y',
    'Z',
  ];
  const duckyCmds = [
    'STRING',
    'STRINGLN',
    'DELAY',
    'ENTER',
    'TAB',
    'SPACE',
    'BACKSPACE',
    'GUI',
    'ALT',
    'CTRL',
    'SHIFT',
    'ESC',
    'DELETE',
    'HOME',
    'END',
    'RSHIFT',
    'CAPSLOCK',
    'UPARROW',
    'DOWNARROW',
    'LEFTARROW',
    'RIGHTARROW',
    'INSERT',
    'NUMLOCK',
    'PRINTSCREEN',
    'SCROLLLOCK',
    'PAGEUP',
    'PAGEDOWN',
    'UP',
    'DOWN',
    'LEFT',
    'RIGHT',
    'BREAK',
    'PAUSE',
    'F1',
    'F2',
    'F3',
    'F4',
    'F5',
    'F6',
    'F7',
    'F8',
    'F9',
    'F10',
    'F11',
    'F12',
    'F13',
    'F14',
    'F15',
    'F16',
    'F17',
    'F18',
    'F19',
    'F20',
    'F21',
    'F22',
    'F23',
    'F24',
    'MK_VOLUP',
    'MK_VOLDOWN',
    'MK_MUTE',
    'MK_NEXT',
    'MK_PREV',
    'MK_PP',
    'MK_STOP',
    'MOUSE_CLICK',
    'MOUSE_PRESS',
    'MOUSE_RELEASE',
    'MOUSE_MOVE',
    'MOUSE_SCROLL',
    'JIGGLE_MOUSE',
    'BACKGROUND_JIGGLE_MOUSE',
    'REPEAT',
    'IMPORT',
    'PRINT',
    'SELECT_LAYOUT',
    'HOLD',
    'RELEASE',
    'RELEASE_ALL',
    'DEFAULT_DELAY',
    'DEFAULTDELAY',
    'RESTART_PAYLOAD',
    'STOP_PAYLOAD',
    'DISABLE_STRIP',
    'ENABLE_STRIP',
    'RESET',
    'RESET_SAFE',
    'RESET_UF2',
    'SET_RESET_NORMAL',
    'SET_RESET_SAFE',
    'SET_RESET_UF2',
    'FORMAT',
    'ENABLE_DEBUG',
    'DISABLE_DEBUG',
    'WINDOWS',
    'COMMAND',
    'RGUI',
    'RIGHT_GUI',
    'RCOMMAND',
    'RWINDOWS',
    'RIGHT_SHIFT',
    'CONTROL',
    'RCTRL',
    'RIGHT_CONTROL',
    'RALT',
    'RIGHT_ALT',
    'OPTION',
    'ROPTION',
    'APP',
    'MENU',
    'ATTACKMODE',
    'LED_ON',
    'LED_R',
    'LED_G',
    'LED_OFF',
    'WAIT_FOR_CAPS_ON',
    'WAIT_FOR_CAPS_OFF',
    'WAIT_FOR_CAPS_CHANGE',
    'WAIT_FOR_NUM_ON',
    'WAIT_FOR_NUM_OFF',
    'WAIT_FOR_NUM_CHANGE',
    'WAIT_FOR_SCROLL_ON',
    'WAIT_FOR_SCROLL_OFF',
    'WAIT_FOR_SCROLL_CHANGE',
    'RANDOM_DELAY',
  ];

  const controlCmds = [
    'VAR',
    'DEFINE',
    'FUNCTION',
    'END_FUNCTION',
    'IF',
    'ELSE_IF',
    'ELSEIF',
    'ELSE',
    'END_IF',
    'WHILE',
    'END_WHILE',
    'STRING_BLOCK',
    'END_STRING',
    'STRINGLN_BLOCK',
    'END_STRINGLN',
    'REM_BLOCK',
    'END_REM',
  ];

  const commandDocs = {
    // ----- actions / keystrokes -----
    STRING: 'Types the specified text layout sequence',
    STRINGLN: 'Types the specified text followed by a newline',
    DELAY: 'Halts payload processing for specified milliseconds',
    DEFAULT_DELAY: 'Sets the default delay between lines (ms)',
    DEFAULTDELAY: 'Alias for DEFAULT_DELAY',
    ENTER: 'Executes standard Enter key event',
    TAB: 'Presses the Tab key',
    SPACE: 'Presses the Spacebar',
    BACKSPACE: 'Presses the Backspace key',
    GUI: 'Actuates the primary System Meta Key (Windows/Command)',
    ALT: 'Presses the Alt (Option) key',
    CTRL: 'Presses the Control key',
    SHIFT: 'Presses the Shift key',
    ESC: 'Presses the Escape key',
    DELETE: 'Presses the Delete key',
    HOME: 'Presses the Home key',
    END: 'Presses the End key',
    INSERT: 'Presses the Insert key',
    PAGEUP: 'Presses the Page Up key',
    PAGEDOWN: 'Presses the Page Down key',
    UPARROW: 'Presses the Up Arrow key',
    DOWNARROW: 'Presses the Down Arrow key',
    LEFTARROW: 'Presses the Left Arrow key',
    RIGHTARROW: 'Presses the Right Arrow key',
    UP: 'Presses the Up Arrow key (alias)',
    DOWN: 'Presses the Down Arrow key (alias)',
    LEFT: 'Presses the Left Arrow key (alias)',
    RIGHT: 'Presses the Right Arrow key (alias)',
    CAPSLOCK: 'Toggles Caps Lock',
    NUMLOCK: 'Toggles Num Lock',
    SCROLLLOCK: 'Toggles Scroll Lock',
    PRINTSCREEN: 'Presses the Print Screen key',
    PAUSE: 'Presses the Pause key',
    BREAK: 'Presses the Break key',
    APP: 'Presses the Application / Menu key',
    MENU: 'Alias for APP / Menu key',

    // ----- modifier keys (hold / release) -----
    RSHIFT: 'Right Shift key',
    RIGHT_SHIFT: 'Alias for RSHIFT',
    CONTROL: 'Control key (alias for CTRL)',
    RCTRL: 'Right Control key',
    RIGHT_CONTROL: 'Alias for RCTRL',
    RALT: 'Right Alt key',
    RIGHT_ALT: 'Alias for RALT',
    OPTION: 'Option key (Mac alias for Alt)',
    ROPTION: 'Right Option key',
    WINDOWS: 'Windows key (alias for GUI)',
    COMMAND: 'Command key (Mac alias for GUI)',
    RGUI: 'Right GUI key',
    RIGHT_GUI: 'Alias for RGUI',
    RCOMMAND: 'Right Command key',
    RWINDOWS: 'Right Windows key',

    // ----- function keys -----
    F1: 'F1 key',
    F2: 'F2 key',
    F3: 'F3 key',
    F4: 'F4 key',
    F5: 'F5 key',
    F6: 'F6 key',
    F7: 'F7 key',
    F8: 'F8 key',
    F9: 'F9 key',
    F10: 'F10 key',
    F11: 'F11 key',
    F12: 'F12 key',
    F13: 'F13 key',
    F14: 'F14 key',
    F15: 'F15 key',
    F16: 'F16 key',
    F17: 'F17 key',
    F18: 'F18 key',
    F19: 'F19 key',
    F20: 'F20 key',
    F21: 'F21 key',
    F22: 'F22 key',
    F23: 'F23 key',
    F24: 'F24 key',

    // ----- multimedia keys -----
    MK_VOLUP: 'Volume Up',
    MK_VOLDOWN: 'Volume Down',
    MK_MUTE: 'Mute',
    MK_NEXT: 'Next Track',
    MK_PREV: 'Previous Track',
    MK_PP: 'Play / Pause',
    MK_STOP: 'Stop',

    // ----- mouse -----
    MOUSE_CLICK: 'Click a mouse button (LEFT, RIGHT, MIDDLE)',
    MOUSE_PRESS: 'Press and hold a mouse button',
    MOUSE_RELEASE: 'Release a mouse button',
    MOUSE_MOVE: 'Move the mouse cursor (x y)',
    MOUSE_SCROLL: 'Scroll the mouse wheel (positive = up)',
    JIGGLE_MOUSE: 'Jiggle the mouse for a duration',
    BACKGROUND_JIGGLE_MOUSE:
      'Jiggle the mouse in the background (infinite with INF)',

    // ----- control structures / flow -----
    REPEAT: 'Repeat previous lines (LINES=…, TIMES=…)',
    IF: 'Evaluates a logical condition; executes block if true',
    ELSE_IF: 'Alternative condition in an IF block',
    ELSEIF: 'Alias for ELSE_IF',
    ELSE: 'Fallback block when no IF/ELSE_IF condition is true',
    END_IF: 'Closes an IF block',
    WHILE: 'Loops while the condition is true',
    END_WHILE: 'Closes a WHILE loop',
    FUNCTION: 'Defines a reusable block of code',
    END_FUNCTION: 'Closes a FUNCTION definition',
    VAR: 'Declares a mutable variable',
    DEFINE: 'Assigns an immutable global constant',
    PRINT: 'Outputs a debug message to the serial console',
    IMPORT: 'Imports code from another file',
    SELECT_LAYOUT: 'Switches keyboard layout (e.g., US, WIN_FR)',

    // ----- string / comment blocks -----
    STRING_BLOCK: 'Opens a multi‑line string block (without Enter)',
    END_STRING: 'Closes a STRING_BLOCK',
    STRINGLN_BLOCK:
      'Opens a multi‑line string block (with newline after each line)',
    END_STRINGLN: 'Closes a STRINGLN_BLOCK',
    REM_BLOCK: 'Opens a multi‑line comment block',
    END_REM: 'Closes a REM_BLOCK',

    // ----- special / device commands -----
    ATTACKMODE: 'Switches USB personality (HID / STORAGE / HID STORAGE)',
    LED_ON: 'Turns the built‑in LED on',
    LED_OFF: 'Turns the built‑in LED off',
    LED_R: 'Turns the red LED on (alias)',
    LED_G: 'Turns the green LED on (alias)',
    HOLD: 'Presses and holds a key',
    RELEASE: 'Releases a previously held key',
    RELEASE_ALL: 'Releases all held keys',
    RESTART_PAYLOAD: 'Restarts the payload from the beginning',
    STOP_PAYLOAD: 'Stops the payload immediately',
    DISABLE_STRIP: 'Disables string stripping',
    ENABLE_STRIP: 'Enables string stripping',
    RESET: 'Resets the device',
    RESET_SAFE: 'Safe reset',
    RESET_UF2: 'Reset into UF2 bootloader mode',
    SET_RESET_NORMAL: 'Set reset type to normal',
    SET_RESET_SAFE: 'Set reset type to safe',
    SET_RESET_UF2: 'Set reset type to UF2',
    FORMAT: 'Formats the storage',
    ENABLE_DEBUG: 'Enables debug output',
    DISABLE_DEBUG: 'Disables debug output',
    RANDOM_DELAY: 'Sleeps a random number of milliseconds (min max)',
    WAIT_FOR_CAPS_ON: 'Pauses until Caps Lock is turned on',
    WAIT_FOR_CAPS_OFF: 'Pauses until Caps Lock is turned off',
    WAIT_FOR_CAPS_CHANGE: 'Pauses until Caps Lock state changes',
    WAIT_FOR_NUM_ON: 'Pauses until Num Lock is turned on',
    WAIT_FOR_NUM_OFF: 'Pauses until Num Lock is turned off',
    WAIT_FOR_NUM_CHANGE: 'Pauses until Num Lock state changes',
    WAIT_FOR_SCROLL_ON: 'Pauses until Scroll Lock is turned on',
    WAIT_FOR_SCROLL_OFF: 'Pauses until Scroll Lock is turned off',
    WAIT_FOR_SCROLL_CHANGE: 'Pauses until Scroll Lock state changes',
  };

  const mouseButtons = ['LEFT', 'RIGHT', 'MIDDLE'];
  const layouts = [
    'US',
    'US_DVO',
    'WIN_FR',
    'WIN_DE',
    'WIN_ES',
    'WIN_IT',
    'WIN_BR',
    'WIN_CZ',
    'WIN_CZ1',
    'WIN_DA',
    'WIN_HU',
    'WIN_PO',
    'WIN_SW',
    'WIN_TR',
    'WIN_UK',
    'MAC_FR',
    'MAC_US',
  ];
  const internalVars = [
    '$_CAPSLOCK_ON',
    '$_NUMLOCK_ON',
    '$_SCROLLLOCK_ON',
    '$_BSSID',
    '$_SSID',
    '$_PASSWD',
    '$_RANDOM_MIN',
    '$_RANDOM_MAX',
    '$_JITTER_ENABLED',
    '$_JITTER_MAX',
    '$_CURRENT_VID',
    '$_CURRENT_PID',
    '$_CURRENT_MANF',
    '$_CURRENT_PROD',
    '$_STRICT',
  ];
  const randomVars = [
    '$_RANDOM_INT',
    '$_RANDOM_NUMBER',
    '$_RANDOM_LOWERCASE_LETTER',
    '$_RANDOM_UPPERCASE_LETTER',
    '$_RANDOM_LETTER',
    '$_RANDOM_SPECIAL',
    '$_RANDOM_CHAR',
  ];

  monaco.languages.register({ id: 'duckyscript' });
  monaco.languages.setMonarchTokensProvider('duckyscript', {
    ignoreCase: true,
    keywords: duckyCmds,
    controls: controlCmds,
    constants: [...mouseButtons, ...layouts],
    tokenizer: {
      root: [
        [/\/\*/, 'comment', '@comment'],
        [/REM_BLOCK/, 'keyword', '@rem_block'],
        [/STRINGLN_BLOCK/, 'keyword', '@stringln_block'],
        [/STRING_BLOCK/, 'keyword', '@string_block'],
        [/REM.*$/, 'comment'],
        [/\/\/.*$/, 'comment'],
        [/\$[a-zA-Z_][a-zA-Z0-9_]*/, 'variable'],
        [/@[a-zA-Z_][a-zA-Z0-9_]*/, 'constant'],
        [/\$_[A-Z_0-9:]+/, 'variable.predefined'],
        [/\b\d+\b/, 'number'],
        [/"([^"\\]|\\.)*$/, 'string.invalid'],
        [/"/, 'string', '@string_double'],
        [/'([^'\\]|\\.)*$/, 'string.invalid'],
        [/'/, 'string', '@string_single'],
        [/[=<>!]=?/, 'operator'],
        [/[+\-*\/]/, 'operator'],

        // --- keyword guard: prevent IF/WHILE/FUNCTION/ELSE_IF from being
        //     eaten as function calls when followed by '('  ---
        [/\b(IF|WHILE|ELSE_IF|ELSEIF|FUNCTION)\s*(?=\()/i, 'keyword.control'],

        // function call (for normal identifiers followed by '(' )
        [
          /[a-zA-Z_][a-zA-Z0-9_]*\s*\(/,
          { token: 'identifier', next: '@function_call' },
        ],

        // individual parentheses – catch leftovers from the guard or standalone
        [/\(/, 'delimiter.parenthesis'],
        [/\)/, 'delimiter.parenthesis'],

        // general identifier rule (fallback)
        [
          /[a-zA-Z_][a-zA-Z0-9_]*/,
          {
            cases: {
              '@controls': 'keyword.control',
              '@keywords': 'keyword',
              '@constants': 'constant',
              '@default': 'identifier',
            },
          },
        ],
      ],
      function_call: [
        [/\)/, { token: 'delimiter', next: '@pop' }],
        [/[^)]+/, 'parameter'],
      ],
      comment: [
        [/[^\/*]+/, 'comment'],
        [/\*\//, 'comment', '@pop'],
        [/[\/*]/, 'comment'],
      ],
      rem_block: [
        [/END_REM\b/, 'keyword', '@pop'],
        [/.*/, 'comment'],
      ],
      string_double: [
        [/[^\\"]+/, 'string'],
        [/\\./, 'string.escape'],
        [/"/, 'string', '@pop'],
      ],
      string_single: [
        [/[^\\']+/, 'string'],
        [/\\./, 'string.escape'],
        [/'/, 'string', '@pop'],
      ],
      string_block: [
        [/END_STRING\b/, 'keyword', '@pop'],
        [/.*/, 'string'],
      ],
      stringln_block: [
        [/END_STRINGLN\b/, 'keyword', '@pop'],
        [/.*/, 'string'],
      ],
    },
  });

  monaco.languages.setLanguageConfiguration('duckyscript', {
    comments: { lineComment: 'REM', blockComment: ['/*', '*/'] },
    brackets: [
      ['(', ')'],
      ['[', ']'],
      ['{', '}'],
    ],
    autoClosingPairs: [
      { open: '(', close: ')' },
      { open: '[', close: ']' },
      { open: '{', close: '}' },
      { open: '"', close: '"' },
      { open: "'", close: "'" },
    ],
  });

  // === CODE FOLDING ===
  monaco.languages.registerFoldingRangeProvider('duckyscript', {
    provideFoldingRanges: (model) => {
      const lines = model.getLinesContent();
      const stack = []; // { type, startLine }
      const folds = [];

      const startRegex =
        /^\s*(IF|WHILE|FUNCTION|STRING_BLOCK|STRINGLN_BLOCK|REM_BLOCK)\b/i;
      const endRegex =
        /^\s*(END_IF|END_WHILE|END_FUNCTION|END_STRING|END_STRINGLN|END_REM)\b/i;

      for (let i = 0; i < lines.length; i++) {
        const trimmed = lines[i].trim();
        const startMatch = trimmed.match(startRegex);
        if (startMatch) {
          stack.push({ type: startMatch[1].toUpperCase(), startLine: i + 1 });
        }
        const endMatch = trimmed.match(endRegex);
        if (endMatch) {
          const endType = endMatch[1].toUpperCase();
          for (let j = stack.length - 1; j >= 0; j--) {
            const s = stack[j];
            if (
              (endType === 'END_IF' && s.type === 'IF') ||
              (endType === 'END_WHILE' && s.type === 'WHILE') ||
              (endType === 'END_FUNCTION' && s.type === 'FUNCTION') ||
              (endType === 'END_STRING' && s.type === 'STRING_BLOCK') ||
              (endType === 'END_STRINGLN' && s.type === 'STRINGLN_BLOCK') ||
              (endType === 'END_REM' && s.type === 'REM_BLOCK')
            ) {
              folds.push({
                start: s.startLine,
                end: i + 1,
                kind: monaco.languages.FoldingRangeKind.Region,
              });
              stack.splice(j); // remove matched start and any later incomplete ones
              break;
            }
          }
        }
      }
      return folds;
    },
  });
  // === SIGNATURE HELP ===
  monaco.languages.registerSignatureHelpProvider('duckyscript', {
    signatureHelpTriggerCharacters: ['(', ','],
    provideSignatureHelp: (model, position) => {
      // Word immediately before the '(' or ','
      const line = model.getLineContent(position.lineNumber);
      const textBefore = line.substring(0, position.column - 1);
      const wordMatch = textBefore.match(/([a-zA-Z_][a-zA-Z0-9_]*)\s*$/);
      if (!wordMatch) return null;
      const funcName = wordMatch[1].toUpperCase();

      // ---- built‑in IF / WHILE ----
      if (
        funcName === 'IF' ||
        funcName === 'ELSE_IF' ||
        funcName === 'ELSEIF'
      ) {
        return {
          value: {
            signatures: [
              {
                label: 'IF (condition)',
                documentation: 'Evaluates a logical expression',
                parameters: [
                  { label: 'condition', documentation: 'Boolean expression' },
                ],
              },
            ],
            activeSignature: 0,
            activeParameter: 0,
          },
          dispose: () => {},
        };
      }
      if (funcName === 'WHILE') {
        return {
          value: {
            signatures: [
              {
                label: 'WHILE (condition)',
                documentation: 'Loops while the condition is true',
                parameters: [
                  { label: 'condition', documentation: 'Boolean expression' },
                ],
              },
            ],
            activeSignature: 0,
            activeParameter: 0,
          },
          dispose: () => {},
        };
      }

      // ---- user‑defined functions ----
      const lines = model.getLinesContent();
      for (const line of lines) {
        const defMatch = line
          .trim()
          .match(/^FUNCTION\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(([^)]*)\)/i);
        if (defMatch && defMatch[1].toUpperCase() === funcName) {
          const rawParams = defMatch[2].trim();
          const paramNames = rawParams
            ? rawParams.split(/\s*,\s*/).map((p) => ({ label: p.trim() }))
            : [];
          return {
            value: {
              signatures: [
                {
                  label: `${defMatch[1]}(${rawParams})`,
                  parameters: paramNames,
                },
              ],
              activeSignature: 0,
              activeParameter: 0,
            },
            dispose: () => {},
          };
        }
      }

      return null; // no signature available
    },
  });

  monaco.languages.registerCompletionItemProvider('duckyscript', {
    triggerCharacters: ['$', '@', ' '],
    provideCompletionItems: (model, position) => {
      const textUntilPos = model.getValueInRange({
        startLineNumber: position.lineNumber,
        startColumn: 1,
        endLineNumber: position.lineNumber,
        endColumn: position.column,
      });
      const lineContent = model.getLineContent(position.lineNumber);
      const charBeforeCursor =
        position.column > 1 ? lineContent[position.column - 2] : '';
      const endsWithDollar = charBeforeCursor === '$';
      const endsWithAt = charBeforeCursor === '@';

      const isSpaceTrigger = textUntilPos.endsWith(' ');
      if (isSpaceTrigger) {
        const beforeSpace = textUntilPos.slice(0, -1).trim();
        const tokens = beforeSpace.split(/\s+/);
        const lastToken = tokens[tokens.length - 1]?.toUpperCase();
        const firstToken = tokens[0]?.toUpperCase();
        const range = new monaco.Range(
          position.lineNumber,
          position.column,
          position.lineNumber,
          position.column,
        );

        // ----- ATTACKMODE -----
        if (lastToken === 'ATTACKMODE') {
          return {
            suggestions: ['HID', 'STORAGE', 'HID STORAGE', 'STORAGE HID'].map(
              (m) => ({
                label: m,
                kind: monaco.languages.CompletionItemKind.Enum,
                insertText: m,
                range,
                documentation: `USB mode: ${m}`,
              }),
            ),
          };
        }

        // ----- REPEAT -----
        if (firstToken === 'REPEAT') {
          const lineUp = beforeSpace.toUpperCase();
          const hasLines = lineUp.includes('LINES=');
          const hasTimes = lineUp.includes('TIMES=');
          if (!hasLines || !hasTimes) {
            const suggestions = [];
            if (!hasLines)
              suggestions.push({
                label: 'LINES=',
                kind: monaco.languages.CompletionItemKind.Property,
                insertText: ' LINES=',
                range,
                documentation: 'Number of previous lines to repeat',
              });
            if (!hasTimes)
              suggestions.push({
                label: 'TIMES=',
                kind: monaco.languages.CompletionItemKind.Property,
                insertText: ' TIMES=',
                range,
                documentation: 'Number of times to repeat those lines',
              });
            return { suggestions };
          }
          return { suggestions: [] };
        }

        // ----- Mouse button completions -----
        if (
          lastToken === 'MOUSE_CLICK' ||
          lastToken === 'MOUSE_PRESS' ||
          lastToken === 'MOUSE_RELEASE'
        ) {
          return {
            suggestions: mouseButtons.map((b) => ({
              label: b,
              kind: monaco.languages.CompletionItemKind.Enum,
              insertText: b,
              range,
              documentation: `${lastToken} ${b}`,
            })),
          };
        }

        // ----- SELECT_LAYOUT -----
        if (lastToken === 'SELECT_LAYOUT') {
          return {
            suggestions: layouts.map((l) => ({
              label: l,
              kind: monaco.languages.CompletionItemKind.Constant,
              insertText: l,
              range,
              documentation: `Switch to ${l} layout`,
            })),
          };
        }

        // ----- HOLD / RELEASE -----
        if (lastToken === 'HOLD' || lastToken === 'RELEASE') {
          return {
            suggestions: holdKeys.map((k) => ({
              label: k,
              kind: monaco.languages.CompletionItemKind.Keyword,
              insertText: k,
              range,
              documentation: `${lastToken} ${k}`,
            })),
          };
        }

        // ----- Delay commands (snippet placeholders) -----
        if (lastToken === 'DELAY') {
          return {
            suggestions: [
              {
                label: 'DELAY ms',
                kind: monaco.languages.CompletionItemKind.Snippet,
                insertText: ' ${1:1000}',
                insertTextRules:
                  monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
                range,
                documentation: 'Delay in milliseconds',
              },
            ],
          };
        }

        if (lastToken === 'RANDOM_DELAY') {
          return {
            suggestions: [
              {
                label: 'RANDOM_DELAY min max',
                kind: monaco.languages.CompletionItemKind.Snippet,
                insertText: ' ${1:100} ${2:500}',
                insertTextRules:
                  monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
                range,
                documentation: 'Random delay between min and max ms',
              },
            ],
          };
        }

        if (lastToken === 'DEFAULT_DELAY' || lastToken === 'DEFAULTDELAY') {
          return {
            suggestions: [
              {
                label: 'DEFAULT_DELAY ms',
                kind: monaco.languages.CompletionItemKind.Snippet,
                insertText: ' ${1:50}',
                insertTextRules:
                  monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
                range,
                documentation: 'Default delay between lines',
              },
            ],
          };
        }

        // ----- Mouse move (x y) -----
        if (lastToken === 'MOUSE_MOVE') {
          return {
            suggestions: [
              {
                label: 'MOUSE_MOVE x y',
                kind: monaco.languages.CompletionItemKind.Snippet,
                insertText: ' ${1:0} ${2:0}',
                insertTextRules:
                  monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
                range,
                documentation: 'Move mouse to absolute coordinates',
              },
            ],
          };
        }

        // ----- MOUSE_SCROLL (amount) -----
        if (lastToken === 'MOUSE_SCROLL') {
          return {
            suggestions: [
              {
                label: 'MOUSE_SCROLL amount',
                kind: monaco.languages.CompletionItemKind.Snippet,
                insertText: ' ${1:1}',
                insertTextRules:
                  monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
                range,
                documentation: 'Scroll wheel (positive = up)',
              },
            ],
          };
        }

        // ----- JIGGLE_MOUSE / BACKGROUND_JIGGLE_MOUSE -----
        if (lastToken === 'JIGGLE_MOUSE') {
          return {
            suggestions: [
              {
                label: 'JIGGLE_MOUSE duration [step] [sleep]',
                kind: monaco.languages.CompletionItemKind.Snippet,
                insertText: ' ${1:5000} ${2:1} ${3:0.5}',
                insertTextRules:
                  monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
                range,
                documentation: 'Jiggle mouse for duration (ms)',
              },
            ],
          };
        }

        if (lastToken === 'BACKGROUND_JIGGLE_MOUSE') {
          return {
            suggestions: [
              {
                label: 'BACKGROUND_JIGGLE_MOUSE duration|INF [step] [sleep]',
                kind: monaco.languages.CompletionItemKind.Snippet,
                insertText: ' ${1:INF} ${2:1} ${3:0.5}',
                insertTextRules:
                  monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
                range,
                documentation: 'Background jiggle (use INF for infinite)',
              },
            ],
          };
        }

        return { suggestions: [] };
      }

      // ---- Block expansion snippets (saved to be added later) ----
      const word = model.getWordUntilPosition(position);
      const currentWord = word ? word.word : '';
      const wordRange = new monaco.Range(
        position.lineNumber,
        word.startColumn,
        position.lineNumber,
        word.endColumn,
      );

      const blockSnippets = {
        IF: {
          snippet: 'IF (${1:condition})\n    $2\nEND_IF',
          doc: 'If block',
          end: 'END_IF',
        },
        WHILE: {
          snippet: 'WHILE (${1:condition})\n    $2\nEND_WHILE',
          doc: 'While loop',
          end: 'END_WHILE',
        },

        FUNCTION: {
          snippet: 'FUNCTION ${1:name}()\n    $2\nEND_FUNCTION',
          doc: 'Function definition',
          end: 'END_FUNCTION',
        },

        STRING_BLOCK: {
          snippet: 'STRING_BLOCK\n    $1\nEND_STRING',
          doc: 'Multi‑line text without Enter',
          end: 'END_STRING',
        },
        STRINGLN_BLOCK: {
          snippet: 'STRINGLN_BLOCK\n    $1\nEND_STRINGLN',
          doc: 'Multi‑line text with Enter',
          end: 'END_STRINGLN',
        },
        REM_BLOCK: {
          snippet: 'REM_BLOCK\n    $1\nEND_REM',
          doc: 'Comment block',
          end: 'END_REM',
        },
      };

      const blockSuggestions = [];
      const upperWord = currentWord.toUpperCase();
      for (const [key, cfg] of Object.entries(blockSnippets)) {
        if (key.startsWith(upperWord)) {
          blockSuggestions.push({
            label: `${key} … ${cfg.end}`,
            kind: monaco.languages.CompletionItemKind.Snippet,
            insertText: cfg.snippet,
            insertTextRules:
              monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
            range: wordRange,
            documentation: cfg.doc,
          });
        }
      }

      let range;
      if (endsWithDollar || endsWithAt) {
        range = new monaco.Range(
          position.lineNumber,
          position.column,
          position.lineNumber,
          position.column,
        );
      } else {
        const word = model.getWordUntilPosition(position);
        range = new monaco.Range(
          position.lineNumber,
          word.startColumn,
          position.lineNumber,
          word.endColumn,
        );
      }

      const suggestions = [];
      const lines = model.getLinesContent();
      const userConsts = new Set(),
        userVars = new Set();
      lines.forEach((line) => {
        const dm = line.trim().match(/^DEFINE\s+([a-zA-Z_@][a-zA-Z0-9_]*)/i);
        if (dm) userConsts.add(dm[1]);
        const vm = line.trim().match(/^(?:VAR\s+)?(\$[a-zA-Z_][a-zA-Z0-9_]*)/i);
        if (vm) userVars.add(vm[1]);
      });

      userConsts.forEach((c) => {
        let insertText = c,
          useRange = range;
        if (endsWithAt && c.startsWith('@')) {
          insertText = c.slice(1);
          useRange = new monaco.Range(
            position.lineNumber,
            position.column,
            position.lineNumber,
            position.column,
          );
        }
        suggestions.push({
          label: c,
          kind: monaco.languages.CompletionItemKind.Constant,
          insertText,
          range: useRange,
          documentation: `User constant: ${c}`,
        });
      });

      userVars.forEach((v) => {
        let insertText = v,
          useRange = range;
        if ((endsWithDollar || endsWithAt) && v.startsWith('$')) {
          insertText = v.slice(1);
          useRange = new monaco.Range(
            position.lineNumber,
            position.column,
            position.lineNumber,
            position.column,
          );
        }
        suggestions.push({
          label: v,
          kind: monaco.languages.CompletionItemKind.Variable,
          insertText,
          range: useRange,
          documentation: `User variable: ${v}`,
        });
      });
      duckyCmds.forEach((cmd) =>
        suggestions.push({
          label: cmd,
          kind: monaco.languages.CompletionItemKind.Keyword,
          insertText: cmd,
          range,
          documentation: commandDocs[cmd] || `Command: ${cmd}`,
        }),
      );
      controlCmds.forEach((cmd) =>
        suggestions.push({
          label: cmd,
          kind: monaco.languages.CompletionItemKind.Keyword,
          insertText: cmd,
          range,
          documentation: commandDocs[cmd] || `Control: ${cmd}`,
        }),
      );

      mouseButtons.forEach((b) =>
        suggestions.push({
          label: b,
          kind: monaco.languages.CompletionItemKind.Enum,
          insertText: b,
          range,
          documentation: `Mouse button: ${b}`,
        }),
      );
      [...internalVars, ...randomVars].forEach((v) => {
        let insertText = v,
          useRange = range;
        if ((endsWithDollar || endsWithAt) && v.startsWith('$')) {
          insertText = v.slice(1);
          useRange = new monaco.Range(
            position.lineNumber,
            position.column,
            position.lineNumber,
            position.column,
          );
        }
        suggestions.push({
          label: v,
          kind: monaco.languages.CompletionItemKind.Variable,
          insertText,
          range: useRange,
          documentation: `System variable: ${v}`,
        });
      });
      layouts.forEach((l) =>
        suggestions.push({
          label: l,
          kind: monaco.languages.CompletionItemKind.Constant,
          insertText: l,
          range,
          documentation: `Layout: ${l}`,
        }),
      );

      if (blockSuggestions.length > 0) {
        suggestions.unshift(...blockSuggestions);
      }
      return { suggestions };
    },
  });

  // === HOVER TOOLTIPS ===
  monaco.languages.registerHoverProvider('duckyscript', {
    provideHover: (model, position) => {
      const word = model.getWordAtPosition(position);
      if (!word) return null;

      const upperWord = word.word.toUpperCase();

      // Check built‑in commands / controls
      const doc = commandDocs[upperWord];
      if (doc) {
        return {
          range: new monaco.Range(
            position.lineNumber,
            word.startColumn,
            position.lineNumber,
            word.endColumn,
          ),
          contents: [{ value: `**${word.word}** – ${doc}` }],
        };
      }

      // Optionally show info for user‑defined constants/variables (heuristic)
      // You can extend this later with actual parsed symbol info.
      return null;
    },
  });

  const fullCommandSet = new Set([...duckyCmds, ...controlCmds]);

  function performScriptValidation(model) {
    model = model || editor.getModel();
    if (!model) return;
    const lines = model.getLinesContent();
    const markers = [],
      userFuncs = new Set(),
      blockStack = [];
    let insideStringBlock = false,
      insideRemBlock = false,
      insideBlockComment = false;
    let constCount = 0,
      varCount = 0,
      totalTimeMs = 0,
      defaultDelay = 0;
    const definesMap = {};

    for (const line of lines) {
      const m = line.trim().match(/^FUNCTION\s+([a-zA-Z_][a-zA-Z0-9_]*)/i);
      if (m) userFuncs.add(m[1].toUpperCase());
      const dm = line
        .trim()
        .match(/^DEFINE\s+([a-zA-Z_@][a-zA-Z0-9_]*)\s+(.+)/i);
      if (dm) definesMap[dm[1].toUpperCase()] = dm[2].trim();
    }
    for (const line of lines) {
      const dm = line.trim().match(/^(?:DEFAULT_DELAY|DEFAULTDELAY)\s+(.+)/i);
      if (dm) {
        const raw = dm[1].trim().toUpperCase();
        const val = definesMap[raw] || raw;
        const num = parseInt(val, 10);
        if (!isNaN(num)) defaultDelay = num;
      }
    }
    function resolveDefineValue(token) {
      token = token.trim();
      const upper = token.toUpperCase();
      if (definesMap[upper]) return resolveDefineValue(definesMap[upper]);
      const num = parseInt(token, 10);
      return isNaN(num) ? token : num;
    }

    const funcDefs = [],
      defineDefs = [],
      varDefs = [];

    for (let idx = 0; idx < lines.length; idx++) {
      const lineContent = lines[idx];
      const lineNum = idx + 1;
      const trimmed = lineContent.trim();
      if (!trimmed) continue;

      if (/^DEFINE\s+/i.test(trimmed)) constCount++;
      else if (
        /^VAR\s+/i.test(trimmed) ||
        /^\$[a-zA-Z_][a-zA-Z0-9_]*\s*=/i.test(trimmed)
      )
        varCount++;

      if (insideRemBlock) {
        if (/END_REM/i.test(trimmed)) insideRemBlock = false;
        continue;
      }
      if (/^REM_BLOCK/i.test(trimmed)) {
        insideRemBlock = true;
        continue;
      }
      if (insideBlockComment) {
        if (trimmed.includes('*/')) insideBlockComment = false;
        continue;
      }
      if (trimmed.includes('/*')) {
        if (!trimmed.includes('*/')) insideBlockComment = true;
        continue;
      }
      if (trimmed.startsWith('REM') || trimmed.startsWith('//')) continue;

      const upperTrim = trimmed.toUpperCase();
      const isStringBlockStart =
        upperTrim === 'STRING_BLOCK' || upperTrim === 'STRINGLN_BLOCK';
      if (isStringBlockStart && !insideStringBlock) {
        insideStringBlock = true;
        blockStack.push({ type: 'STRING_BLOCK', line: lineNum });
        continue;
      }
      if (insideStringBlock) {
        if (upperTrim === 'END_STRING' || upperTrim === 'END_STRINGLN') {
          insideStringBlock = false;
          const top = blockStack.pop();
          if (!top || top.type !== 'STRING_BLOCK')
            markers.push({
              severity: monaco.MarkerSeverity.Error,
              message: `Mismatched block terminal: "${trimmed}"`,
              startLineNumber: lineNum,
              startColumn: 1,
              endLineNumber: lineNum,
              endColumn: lineContent.length + 1,
            });
        }
        continue;
      }

      const funcMatch = trimmed.match(/^FUNCTION\s+([a-zA-Z_][a-zA-Z0-9_]*)/i);
      if (funcMatch)
        funcDefs.push({ name: funcMatch[1].toUpperCase(), line: lineNum });
      const defineMatch = trimmed.match(/^DEFINE\s+([a-zA-Z_@][a-zA-Z0-9_]*)/i);
      if (defineMatch)
        defineDefs.push({ name: defineMatch[1].toUpperCase(), line: lineNum });

      const varMatch = trimmed.match(
        /^(?:VAR\s+)?(\$[a-zA-Z_][a-zA-Z0-9_]*)\s*=/i,
      );
      if (varMatch) {
        const varName = varMatch[1];
        // never flag built-in / random variables as unused
        if (!internalVars.includes(varName) && !randomVars.includes(varName)) {
          varDefs.push({ name: varName, line: lineNum });
        }
      }

      if (defaultDelay > 0) totalTimeMs += defaultDelay;
      const dMatch = trimmed.match(/^DELAY\s+(.+)/i);
      if (dMatch) {
        const raw = dMatch[1].trim().toUpperCase();
        const val = resolveDefineValue(raw);
        const num = parseInt(val, 10);
        if (!isNaN(num)) totalTimeMs += num;
      }

      const firstToken = trimmed.split(/\s+/)[0];
      const firstTokenUpper = firstToken.toUpperCase();
      if (
        firstTokenUpper === 'IF' ||
        firstTokenUpper === 'WHILE' ||
        firstTokenUpper === 'FUNCTION'
      ) {
        blockStack.push({ type: firstTokenUpper, line: lineNum });
      } else if (
        firstTokenUpper === 'ELSE_IF' ||
        firstTokenUpper === 'ELSEIF' ||
        firstTokenUpper === 'ELSE'
      ) {
        const top = blockStack[blockStack.length - 1];
        if (!top || top.type !== 'IF')
          markers.push({
            severity: monaco.MarkerSeverity.Error,
            message: `${firstTokenUpper} outside active IF sequence`,
            startLineNumber: lineNum,
            startColumn: 1,
            endLineNumber: lineNum,
            endColumn: lineContent.length + 1,
          });
      } else if (firstTokenUpper === 'END_IF') {
        const top = blockStack.pop();
        if (!top || top.type !== 'IF')
          markers.push({
            severity: monaco.MarkerSeverity.Error,
            message: 'END_IF without matching IF',
            startLineNumber: lineNum,
            startColumn: 1,
            endLineNumber: lineNum,
            endColumn: lineContent.length + 1,
          });
      } else if (firstTokenUpper === 'END_WHILE') {
        const top = blockStack.pop();
        if (!top || top.type !== 'WHILE')
          markers.push({
            severity: monaco.MarkerSeverity.Error,
            message: 'END_WHILE without matching WHILE',
            startLineNumber: lineNum,
            startColumn: 1,
            endLineNumber: lineNum,
            endColumn: lineContent.length + 1,
          });
      } else if (firstTokenUpper === 'END_FUNCTION') {
        const top = blockStack.pop();
        if (!top || top.type !== 'FUNCTION')
          markers.push({
            severity: monaco.MarkerSeverity.Error,
            message: 'END_FUNCTION without matching FUNCTION',
            startLineNumber: lineNum,
            startColumn: 1,
            endLineNumber: lineNum,
            endColumn: lineContent.length + 1,
          });
      }

      const isFunctionCall = /^[a-zA-Z_][a-zA-Z0-9_]*\s*\(/.test(trimmed);
      const opAssign = trimmed.startsWith('$') || trimmed.startsWith('@');
      const verifiable =
        fullCommandSet.has(firstTokenUpper) ||
        userFuncs.has(firstTokenUpper) ||
        isFunctionCall;
      if (
        !verifiable &&
        !opAssign &&
        !trimmed.startsWith('/*') &&
        !trimmed.startsWith('*')
      ) {
        markers.push({
          severity: monaco.MarkerSeverity.Error,
          message: `Unrecognized token: "${firstToken}"`,
          startLineNumber: lineNum,
          startColumn: lineContent.indexOf(firstToken) + 1,
          endLineNumber: lineNum,
          endColumn: lineContent.indexOf(firstToken) + firstToken.length + 1,
        });
      }
    }

    for (const b of blockStack) {
      markers.push({
        severity: monaco.MarkerSeverity.Error,
        message: `Unclosed block "${b.type}" from line ${b.line}`,
        startLineNumber: b.line,
        startColumn: 1,
        endLineNumber: b.line,
        endColumn: 50,
      });
    }

    const unusedRanges = [];
    funcDefs.forEach((fd) => {
      const name = fd.name,
        defLine = fd.line;
      let used = false;
      const tokenRegex = new RegExp(`\\b${name}\\b`, 'i'),
        callRegex = new RegExp(`${name}\\s*\\(`, 'i');
      for (let i = 0; i < lines.length; i++) {
        if (i + 1 === defLine) continue;
        if (callRegex.test(lines[i]) || tokenRegex.test(lines[i])) {
          used = true;
          break;
        }
      }
      if (!used) {
        markers.push({
          severity: monaco.MarkerSeverity.Info,
          message: `Unused function '${fd.name}'`,
          startLineNumber: defLine,
          startColumn: 1,
          endLineNumber: defLine,
          endColumn: lines[defLine - 1].length + 1,
        });
        unusedRanges.push({
          range: new monaco.Range(
            defLine,
            1,
            defLine,
            lines[defLine - 1].length + 1,
          ),
          options: { inlineClassName: 'unused-symbol' },
        });
      }
    });
    defineDefs.forEach((dd) => {
      const name = dd.name,
        defLine = dd.line;
      let used = false;
      const isAtDefine = name.startsWith('@');
      const tokenRegex = isAtDefine ? null : new RegExp(`\\b${name}\\b`, 'i');
      for (let i = 0; i < lines.length; i++) {
        if (i + 1 === defLine) continue;
        if (isAtDefine ? lines[i].includes(name) : tokenRegex.test(lines[i])) {
          used = true;
          break;
        }
      }

      if (!used) {
        markers.push({
          severity: monaco.MarkerSeverity.Info,
          message: `Unused constant '${dd.name}'`,
          startLineNumber: defLine,
          startColumn: 1,
          endLineNumber: defLine,
          endColumn: lines[defLine - 1].length + 1,
        });
        unusedRanges.push({
          range: new monaco.Range(
            defLine,
            1,
            defLine,
            lines[defLine - 1].length + 1,
          ),
          options: { inlineClassName: 'unused-symbol' },
        });
      }
    });
    varDefs.forEach((vd) => {
      const name = vd.name,
        defLine = vd.line;
      let used = false;
      for (let i = 0; i < lines.length; i++) {
        if (i + 1 === defLine) continue;
        if (lines[i].includes(name)) {
          used = true;
          break;
        }
      }
      if (!used) {
        markers.push({
          severity: monaco.MarkerSeverity.Info,
          message: `Unused variable '${name}'`,
          startLineNumber: defLine,
          startColumn: 1,
          endLineNumber: defLine,
          endColumn: lines[defLine - 1].length + 1,
        });
        unusedRanges.push({
          range: new monaco.Range(
            defLine,
            1,
            defLine,
            lines[defLine - 1].length + 1,
          ),
          options: { inlineClassName: 'unused-symbol' },
        });
      }
    });

    monaco.editor.setModelMarkers(model, 'duckyscript', markers);
    const oldDecIds = unusedDecorations.get(model) || [];
    const newDecIds = model.deltaDecorations(oldDecIds, unusedRanges);
    unusedDecorations.set(model, newDecIds);

    document.getElementById('lineCountStatus').textContent =
      `Lines: ${lines.length}`;
    document.getElementById('varCountStatus').textContent =
      `Variables: ${varCount}`;
    document.getElementById('constCountStatus').textContent =
      `Constants: ${constCount}`;
    document.getElementById('runTimeStatus').innerHTML =
      `Est. Run Time: ${(totalTimeMs / 1000).toFixed(1)}s`;
    const statusNode = document.getElementById('validationStatus');
    if (statusNode) {
      const errorCount = markers.filter(
        (m) => m.severity === monaco.MarkerSeverity.Error,
      ).length;
      statusNode.textContent = errorCount
        ? `● Syntax Errors (${errorCount})`
        : '● Syntax Valid';
      statusNode.className = errorCount
        ? 'error-state status-stat-item'
        : 'valid-state status-stat-item';
    }
  }

  const themeFileMap = {
    active4d: 'Active4D',
    'all-hallows-eve': 'All Hallows Eve',
    amy: 'Amy',
    'birds-of-paradise': 'Birds of Paradise',
    blackboard: 'Blackboard',
    'brilliance-black': 'Brilliance Black',
    'brilliance-dull': 'Brilliance Dull',
    'chrome-devtools': 'Chrome DevTools',
    'clouds-midnight': 'Clouds Midnight',
    clouds: 'Clouds',
    cobalt: 'Cobalt',
    cobalt2: 'Cobalt2',
    dawn: 'Dawn',
    dracula: 'Dracula',
    dreamweaver: 'Dreamweaver',
    eiffel: 'Eiffel',
    'espresso-libre': 'Espresso Libre',
    'github-dark': 'GitHub Dark',
    'github-light': 'GitHub Light',
    github: 'GitHub',
    idle: 'IDLE',
    katzenmilch: 'Katzenmilch',
    'kuroir-theme': 'Kuroir Theme',
    lazy: 'LAZY',
    'magicwb--amiga-': 'MagicWB (Amiga)',
    'merbivore-soft': 'Merbivore Soft',
    merbivore: 'Merbivore',
    'monokai-bright': 'Monokai Bright',
    monokai: 'Monokai',
    'night-owl': 'Night Owl',
    nord: 'Nord',
    'oceanic-next': 'Oceanic Next',
    'pastels-on-dark': 'Pastels on Dark',
    'slush-and-poppies': 'Slush and Poppies',
    'solarized-dark': 'Solarized-dark',
    'solarized-light': 'Solarized-light',
    spacecadet: 'SpaceCadet',
    sunburst: 'Sunburst',
    'textmate--mac-classic-': 'Textmate (Mac Classic)',
    'tomorrow-night-blue': 'Tomorrow-Night-Blue',
    'tomorrow-night-bright': 'Tomorrow-Night-Bright',
    'tomorrow-night-eighties': 'Tomorrow-Night-Eighties',
    'tomorrow-night': 'Tomorrow-Night',
    tomorrow: 'Tomorrow',
    twilight: 'Twilight',
    'upstream-sunburst': 'Upstream Sunburst',
    'vibrant-ink': 'Vibrant Ink',
    'xcode-default': 'Xcode_default',
    zenburnesque: 'Zenburnesque',
    iplastic: 'iPlastic',
    idlefingers: 'idleFingers',
    krtheme: 'krTheme',
    monoindustrial: 'monoindustrial',
  };
  const loadedThemes = new Set(['vs', 'vs-dark', 'hc-black']);
  let activeTheme = localStorage.getItem('overquack-ide-theme') || 'monokai';
  const themeSelect = document.getElementById('themeSelect');
  if (themeSelect) {
    themeSelect.innerHTML =
      '<option value="vs">VS</option><option value="vs-dark">VS Dark</option><option value="hc-black">High Contrast (Dark)</option>';
    for (const [id, name] of Object.entries(themeFileMap)) {
      const option = document.createElement('option');
      option.value = id;
      option.textContent = name;
      themeSelect.appendChild(option);
    }
    themeSelect.value = activeTheme;
  }
  function loadTheme(name) {
    if (name === 'vs' || name === 'vs-dark' || name === 'hc-black') {
      monaco.editor.setTheme(name);
      return;
    }
    if (loadedThemes.has(name)) {
      monaco.editor.setTheme(name);
      return;
    }
    const file = themeFileMap[name];
    if (!file) {
      monaco.editor.setTheme('vs-dark');
      return;
    }
    fetch(
      `https://cdn.jsdelivr.net/gh/brijeshb42/monaco-themes@master/themes/${encodeURIComponent(file)}.json`,
    )
      .then((r) => r.json())
      .then((data) => {
        monaco.editor.defineTheme(name, data);
        loadedThemes.add(name);
        monaco.editor.setTheme(name);
      })
      .catch(() => monaco.editor.setTheme('vs-dark'));
  }
  loadTheme(activeTheme);
  if (themeSelect) {
    themeSelect.addEventListener('change', (e) => {
      localStorage.setItem('overquack-ide-theme', e.target.value);
      loadTheme(e.target.value);
    });
  }

  const defaultScript = dedent(`/*
============================================================
    OverQuack Language Demo - Windows Showcase
    Advanced Cross-Platform HID keystrokes injection
    Demonstrates: DEFINE, VAR, IF/ELSE, WHILE, FUNCTION,
    PRINT, STRING, DELAY, GUI, MOUSE, RANDOM vars, etc.
    check "https://github.com/VexilonHacker/OverQuack" for more details. (⌐■_■)
============================================================
*/

REM ---------- Variables & Constants ----------
DEFINE SHORT_DELAY 500
DEFINE LONG_DELAY 1500
DEFAULT_DELAY 100

VAR $username = "OverQuackUser"
VAR $counter = 1
$maxLoops = 3
$token = "JbruJ1v6NK.cFyCksy_OXKn8NbgRG#T44l0V@9ay"

// ---------- Open Notepad (basic GUI interaction) ----------
GUI r
DELAY SHORT_DELAY
STRING notepad
ENTER
DELAY LONG_DELAY

// ---------- STRING and built-in random variables ----------
STRING_BLOCK
WiFi OverQuack Dynamic Framework Context Profile:
- Active Tracker Code: $_RANDOM_NUMBER:8
- Hardware Identity Target Match: $_BSSID
END_STRING

STRING Hello $username, this is a demo of OverQuack!
ENTER
STRING Your random session ID: $_RANDOM_NUMBER:12
ENTER
STRING Your passkey lowercase letter: $_RANDOM_LOWERCASE_LETTER
ENTER
STRING Your secret special char: $_RANDOM_SPECIAL
ENTER

REM ---------- IF / ELSE example ----------
IF $_CAPSLOCK_ON == 1
    PRINT Caps Lock is ON – turning it OFF for demo
    CAPSLOCK
ELSE
    PRINT Caps Lock is OFF – leaving as is
END_IF

REM ---------- WHILE loop with counter ----------
WHILE $counter <= $maxLoops
    PRINT Loop iteration #$counter
    STRINGLN Loop step $counter completed.
    $counter = $counter + 1
    DELAY SHORT_DELAY
END_WHILE

REM ---------- Mouse movement demonstration ----------
// PRINT are used to print msgs to serial console
PRINT Moving mouse to (200, 200)...
MOUSE_MOVE 200 200
DELAY SHORT_DELAY
PRINT Performing left click...
MOUSE_CLICK LEFT
DELAY SHORT_DELAY
PRINT Scrolling down 3 steps...
MOUSE_SCROLL 3

REM ---------- Function definition and call ----------
FUNCTION showEndMessage
    PRINT [DEMO] Function executed.
    STRING All demo features completed successfully!
    ENTER
    STRING Press ENTER to close Notepad...
    ENTER
END_FUNCTION

showEndMessage()

REM_BLOCK
// ---------- Conditional restart (commented for safety) ----------
 IF $_NUMLOCK_ON == 0
     PRINT NumLock is off – restarting demo...
     RESTART_PAYLOAD
END_IF
END_REM

REM ---------- Final cleanup (close Notepad via Alt+F4) ----------
DELAY LONG_DELAY
ALT F4
PRINT Demo finished. Goodbye!
  `);

  let editor;
  let tabList = [],
    activeTabId = null,
    tabIdCounter = 0;
  const tabsBar = document.getElementById('tabs-bar'),
    tabsContainer = document.getElementById('tabs-container'),
    newFileBtn = document.getElementById('new-file-btn');

  function showTabsBar() {
    tabsBar.style.display = 'flex';
    newFileBtn.style.display = 'block';
  }
  function hideTabsBar() {
    tabsBar.style.display = 'none';
    newFileBtn.style.display = 'none';
  }
  function updateTabsBarVisibility() {
    tabList.length >= 2 ? showTabsBar() : hideTabsBar();
  }

  function createTab(name, content, markAsModified = false) {
    const id = ++tabIdCounter;
    const model = monaco.editor.createModel(content, 'duckyscript');
    const tab = { id, name, model, isModified: markAsModified };
    tabList.push(tab);
    let validationTimeout;
    model.onDidChangeContent(() => {
      tab.isModified = true;
      renderTabs();
      if (autoSaveEnabled) saveTabsToStorage();
      clearTimeout(validationTimeout);
      validationTimeout = setTimeout(() => performScriptValidation(model), 300);
    });
    return tab;
  }

  function closeTab(tabId) {
    const idx = tabList.findIndex((t) => t.id === tabId);
    if (idx === -1) return;
    const tab = tabList[idx];
    tab.model.dispose();
    tabList.splice(idx, 1);
    if (tabId === activeTabId) {
      if (tabList.length > 0) switchTab(tabList[Math.max(0, idx - 1)].id);
      else {
        const newTab = createTab('Untitled', '');
        switchTab(newTab.id);
      }
    }
    renderTabs();
    updateTabsBarVisibility();
    if (autoSaveEnabled) saveTabsToStorage();
  }

  function switchTab(tabId) {
    const tab = tabList.find((t) => t.id === tabId);
    if (!tab) return;
    activeTabId = tabId;
    editor.setModel(tab.model);
    performScriptValidation(tab.model);
    renderTabs();
    updateTabsBarVisibility();
  }

  function renderTabs() {
    tabsContainer.innerHTML = '';
    tabList.forEach((tab) => {
      const el = document.createElement('div');
      el.className = 'tab' + (tab.id === activeTabId ? ' active' : '');
      if (tab.isModified) el.classList.add('modified');
      el.setAttribute('draggable', 'true');
      el.dataset.tabId = tab.id;
      const nameSpan = document.createElement('span');
      nameSpan.className = 'tab-name';
      nameSpan.textContent = tab.name;
      nameSpan.title = tab.name;
      nameSpan.addEventListener('click', (e) => {
        e.stopPropagation();
        switchTab(tab.id);
      });
      const closeBtn = document.createElement('span');
      closeBtn.className = 'tab-close';
      closeBtn.innerHTML = '&times;';
      closeBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        closeTab(tab.id);
      });
      el.appendChild(nameSpan);
      el.appendChild(closeBtn);
      tabsContainer.appendChild(el);
    });
  }

  function saveTabsToStorage() {
    const toSave = tabList.map((t) => ({
      id: t.id,
      name: t.name,
      content: t.model.getValue(),
    }));
    localStorage.setItem('overquack_tabs', JSON.stringify(toSave));
  }
  function loadSavedTabs() {
    try {
      const raw = localStorage.getItem('overquack_tabs');
      if (!raw) return null;
      const data = JSON.parse(raw);
      if (!Array.isArray(data) || data.length === 0) return null;
      return data;
    } catch (e) {
      return null;
    }
  }

  let dragSrcTabId = null,
    dragPlaceholder = null;
  function insertDragPlaceholder(afterTabId) {
    removeDragPlaceholder();
    const refTab = tabList.find((t) => t.id === afterTabId);
    if (!refTab) return;
    const refEl = tabsContainer.querySelector(`[data-tab-id="${afterTabId}"]`);
    if (!refEl) return;
    dragPlaceholder = document.createElement('div');
    dragPlaceholder.className = 'tab-placeholder';
    refEl.insertAdjacentElement('afterend', dragPlaceholder);
  }
  function removeDragPlaceholder() {
    if (dragPlaceholder) {
      dragPlaceholder.remove();
      dragPlaceholder = null;
    }
  }

  tabsContainer.addEventListener('dragstart', (e) => {
    const tabEl = e.target.closest('.tab');
    if (!tabEl) return;
    e.stopPropagation();
    dragSrcTabId = Number(tabEl.dataset.tabId);
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/plain', '');
    setTimeout(() => tabEl.classList.add('dragging-tab'), 0);
  });
  tabsContainer.addEventListener('dragend', (e) => {
    const tabEl = e.target.closest('.tab');
    if (tabEl) tabEl.classList.remove('dragging-tab');
    dragSrcTabId = null;
    removeDragPlaceholder();
  });
  tabsContainer.addEventListener('dragover', (e) => {
    e.preventDefault();
    e.stopPropagation();
    e.dataTransfer.dropEffect = 'move';
    const tabEl = e.target.closest('.tab');
    if (
      !tabEl ||
      !dragSrcTabId ||
      Number(tabEl.dataset.tabId) === dragSrcTabId
    ) {
      removeDragPlaceholder();
      return;
    }
    insertDragPlaceholder(Number(tabEl.dataset.tabId));
  });
  tabsContainer.addEventListener('drop', (e) => {
    e.preventDefault();
    e.stopPropagation();
    removeDragPlaceholder();
    const targetTabEl = e.target.closest('.tab');
    if (!targetTabEl || !dragSrcTabId) return;
    const targetId = Number(targetTabEl.dataset.tabId);
    if (targetId === dragSrcTabId) return;
    const srcIdx = tabList.findIndex((t) => t.id === dragSrcTabId),
      targetIdx = tabList.findIndex((t) => t.id === targetId);
    if (srcIdx === -1 || targetIdx === -1) return;
    const [moved] = tabList.splice(srcIdx, 1);
    tabList.splice(targetIdx, 0, moved);
    renderTabs();
    dragSrcTabId = null;
  });

  function initTabs() {
    const saved = loadSavedTabs();
    if (saved) {
      saved.forEach(({ id, name, content }) => {
        const tab = createTab(name, content, false);
        tab.id = id;
      });
      switchTab(tabList[0].id);
    } else {
      const tab = createTab('payload.oqs', defaultScript);
      switchTab(tab.id);
      tab.isModified = false;
    }
    renderTabs();
    updateTabsBarVisibility();
  }

  editor = monaco.editor.create(document.getElementById('editor'), {
    value: '',
    language: 'duckyscript',
    theme: activeTheme,
    automaticLayout: true,
    minimap: { enabled: true },
    fontSize: 14,
    fontLigatures: true,
    smoothScrolling: true,
    cursorBlinking: 'phase',
    cursorSmoothCaretAnimation: 'on',
  });

  initTabs();

  newFileBtn.addEventListener('click', () => {
    const tab = createTab('Untitled', '');
    switchTab(tab.id);
    editor.focus();
  });

  const downloadBtn = document.getElementById('downloadBtn');
  if (downloadBtn) {
    downloadBtn.addEventListener('click', () => {
      const activeTab = tabList.find((t) => t.id === activeTabId);
      if (!activeTab) return;
      const content = activeTab.model.getValue();
      const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = activeTab.name.endsWith('.oqs')
        ? activeTab.name
        : activeTab.name + '.oqs';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    });
  }

  const autoSaveToggle = document.getElementById('autoSaveToggle');
  let autoSaveEnabled = false;
  if (autoSaveToggle) {
    const savedPref = localStorage.getItem('overquack_autosave_pref');
    autoSaveEnabled = savedPref === 'true';
    autoSaveToggle.checked = autoSaveEnabled;
    autoSaveToggle.addEventListener('change', (e) => {
      autoSaveEnabled = e.target.checked;
      localStorage.setItem('overquack_autosave_pref', autoSaveEnabled);
      if (!autoSaveEnabled) localStorage.removeItem('overquack_tabs');
      else saveTabsToStorage();
    });
  }

  const minimapToggle = document.getElementById('minimapToggle');
  if (minimapToggle)
    minimapToggle.addEventListener('change', (e) =>
      editor.updateOptions({ minimap: { enabled: e.target.checked } }),
    );

  let currentErrorIndex = 0;
  const validationStatus = document.getElementById('validationStatus');
  if (validationStatus) {
    monaco.editor.onDidChangeMarkers((uri) => {
      if (uri.toString() === editor.getModel().uri.toString())
        currentErrorIndex = 0;
    });
    validationStatus.addEventListener('click', () => {
      const model = editor.getModel();
      if (!model) return;
      const markers = monaco.editor.getModelMarkers({ resource: model.uri });
      const errors = markers.filter(
        (m) => m.severity === monaco.MarkerSeverity.Error,
      );
      if (errors.length === 0) return;
      if (currentErrorIndex >= errors.length) currentErrorIndex = 0;
      const error = errors[currentErrorIndex];
      const line = error.startLineNumber,
        column = Math.max(1, error.startColumn);
      editor.revealPosition({ lineNumber: line, column });
      editor.setPosition({ lineNumber: line, column });
      editor.focus();
      currentErrorIndex = (currentErrorIndex + 1) % errors.length;
    });
  }

  function resizeCheckboxes() {
    const checkboxes = document.querySelectorAll(
      '.controls-wrapper label input[type="checkbox"]',
    );
    checkboxes.forEach((cb) => {
      cb.style.transform = 'scale(0.7)';
      cb.style.transformOrigin = 'left center';
      cb.style.margin = '0 2px 0 0';
    });
  }
  resizeCheckboxes();

  const dropOverlay = document.getElementById('drop-overlay'),
    dropTarget = document.body;
  if (dropOverlay) {
    dropTarget.addEventListener('dragover', (e) => {
      if (e.target.closest('#tabs-container')) return;
      if (
        e.dataTransfer.types &&
        Array.prototype.indexOf.call(e.dataTransfer.types, 'Files') >= 0
      ) {
        e.preventDefault();
        e.stopPropagation();
        dropOverlay.classList.add('active');
      }
    });
    dropTarget.addEventListener('dragleave', (e) => {
      e.preventDefault();
      e.stopPropagation();
      if (!dropOverlay.contains(e.relatedTarget))
        dropOverlay.classList.remove('active');
    });
    dropTarget.addEventListener('drop', async (e) => {
      if (
        !e.dataTransfer.types ||
        Array.prototype.indexOf.call(e.dataTransfer.types, 'Files') === -1
      )
        return;
      e.preventDefault();
      e.stopPropagation();
      dropOverlay.classList.remove('active');
      const files = e.dataTransfer.files;
      if (files.length === 0) return;
      const file = files[0];
      const ext = file.name.split('.').pop().toLowerCase();
      if (['oqs', 'txt', 'dd', 'duck'].includes(ext)) {
        try {
          const content = await file.text();
          const tab = createTab(file.name, content);
          switchTab(tab.id);
          editor.focus();
        } catch (err) {
          console.error('Failed to read file:', err);
        }
      } else console.warn(`Unsupported file type: .${ext}`);
    });
  }

  const templateModal = document.getElementById('templateModal'),
    templateSearch = document.getElementById('templateSearch'),
    templatesList = document.getElementById('templatesList'),
    templatePreview = document.getElementById('templatePreview'),
    templateActions = document.getElementById('templatePreviewActions'),
    templateTitle = document.getElementById('templateModalTitle');
  let previewEditor = null,
    cursorHideStyle = null;

  function resetTemplateView() {
    if (previewEditor) {
      previewEditor.dispose();
      previewEditor = null;
    }
    if (cursorHideStyle) {
      cursorHideStyle.remove();
      cursorHideStyle = null;
    }
    templatePreview.style.display = 'none';
    templateActions.style.display = 'none';
    templatesList.style.display = '';
    templateSearch.style.display = '';
    templateTitle.innerHTML = 'Template Library';
    templatePreview.innerHTML = '';
    renderTemplates(templateSearch.value);
  }
  function showTemplatePreview(tpl) {
    templatesList.style.display = 'none';
    templateSearch.style.display = 'none';
    templateTitle.innerHTML = `<div style="width:100%;display:flex;justify-content:space-between;"><span>Template: ${tpl.name}</span><span id="customPreviewCloseBtn" style="cursor:pointer;">&times;</span></div>`;
    document.getElementById('customPreviewCloseBtn').onclick = () => {
      templateModal.classList.remove('open');
      resetTemplateView();
    };
    templatePreview.style.display = 'block';
    templatePreview.innerHTML = '';
    previewEditor = monaco.editor.create(templatePreview, {
      value: tpl.code,
      language: 'duckyscript',
      theme: activeTheme,
      readOnly: true,
      automaticLayout: true,
      fontSize: 13,
      lineNumbers: 'off',
      glyphMargin: false,
      folding: false,
      lineDecorationsWidth: 0,
      lineNumbersMinChars: 0,
      minimap: { enabled: false },
      scrollBeyondLastLine: false,
      renderLineHighlight: 'none',
      selectionHighlight: false,
      occurrencesHighlight: false,
      cursorStyle: 'line',
      cursorBlinking: 'solid',
    });
    if (cursorHideStyle) cursorHideStyle.remove();
    cursorHideStyle = document.createElement('style');
    cursorHideStyle.textContent = `#templatePreview .monaco-editor .cursors-layer .cursor { display: none !important; }`;
    document.head.appendChild(cursorHideStyle);
    setTimeout(() => previewEditor.layout(), 50);
    templateActions.style.display = 'flex';
    templateActions.innerHTML = '';
    const loadBtn = document.createElement('button');
    loadBtn.className = 'accent';
    loadBtn.textContent = 'Load Template';
    loadBtn.onclick = () => {
      editor.setValue(tpl.code);
      templateModal.classList.remove('open');
      resetTemplateView();
    };
    const backBtn = document.createElement('button');
    backBtn.className = 'ghost';
    backBtn.textContent = 'Back to List';
    backBtn.onclick = resetTemplateView;
    templateActions.appendChild(loadBtn);
    templateActions.appendChild(backBtn);
  }
  function renderTemplates(filter = '') {
    templatesList.innerHTML = '';
    const lower = filter.toLowerCase();
    const filtered = templatesData.filter(
      (t) =>
        t.name.toLowerCase().includes(lower) ||
        t.desc.toLowerCase().includes(lower),
    );
    if (filtered.length === 0) {
      templatesList.innerHTML =
        '<div style="color:#aaa;padding:20px;text-align:center;">No templates found</div>';
      return;
    }
    filtered.forEach((t) => {
      const el = document.createElement('div');
      el.className = 'template-card';
      el.innerHTML = `<div class="tpl-name">${t.name}</div><div class="tpl-desc">${t.desc}</div>`;
      el.onclick = () => showTemplatePreview(t);
      templatesList.appendChild(el);
    });
  }
  document.getElementById('templatesBtn').onclick = () => {
    templateSearch.value = '';
    resetTemplateView();
    templateModal.classList.add('open');
    setTimeout(() => templateSearch.focus(), 50);
  };
  document.getElementById('closeTemplateModal').onclick = () => {
    templateModal.classList.remove('open');
    resetTemplateView();
  };
  templateSearch.oninput = (e) => renderTemplates(e.target.value);
  templateModal.onclick = (e) => {
    if (e.target === templateModal) {
      templateModal.classList.remove('open');
      resetTemplateView();
    }
  };

  const snippetsBtn = document.getElementById('snippetsBtn'),
    snippetsPanel = document.getElementById('snippetsPanel'),
    closeSnippetsPanel = document.getElementById('closeSnippetsPanel'),
    snippetSearch = document.getElementById('snippetSearch'),
    snippetsListContainer = document.getElementById('snippetsList'),
    resizeHandle = document.getElementById('resize-handle');
  let isSnippetPanelOpen = false;

  function openSnippets() {
    isSnippetPanelOpen = true;
    snippetsPanel.classList.add('open');
    resizeHandle.classList.add('visible');
    snippetsBtn.classList.add('active-btn');
    snippetSearch.value = '';
    renderSnippets('');
    editor.layout();
    setTimeout(() => snippetSearch.focus(), 50);
  }
  function closeSnippets() {
    isSnippetPanelOpen = false;
    snippetsPanel.classList.remove('open');
    resizeHandle.classList.remove('visible');
    snippetsBtn.classList.remove('active-btn');
    editor.layout();
  }
  snippetsBtn.onclick = () =>
    isSnippetPanelOpen ? closeSnippets() : openSnippets();
  closeSnippetsPanel.onclick = closeSnippets;
  snippetSearch.oninput = (e) => renderSnippets(e.target.value);
  function renderSnippets(filter = '') {
    snippetsListContainer.innerHTML = '';
    const lower = filter.toLowerCase();
    const grouped = {};
    snippetsData.forEach((s) => {
      if (
        s.name.toLowerCase().includes(lower) ||
        s.category.toLowerCase().includes(lower)
      ) {
        if (!grouped[s.category]) grouped[s.category] = [];
        grouped[s.category].push(s);
      }
    });
    const cats = Object.keys(grouped);
    if (cats.length === 0) {
      snippetsListContainer.innerHTML =
        '<div style="color:#aaa;padding:15px;text-align:center;">No snippets found</div>';
      return;
    }
    cats.forEach((cat) => {
      const catDiv = document.createElement('div');
      catDiv.className = 'snippet-category';
      catDiv.textContent = cat;
      snippetsListContainer.appendChild(catDiv);
      grouped[cat].forEach((item) => {
        const el = document.createElement('div');
        el.className = 'snippet-item';
        el.textContent = item.name;
        el.onclick = () => {
          const pos = editor.getPosition();
          editor.executeEdits('snippet', [
            {
              range: new monaco.Range(
                pos.lineNumber,
                pos.column,
                pos.lineNumber,
                pos.column,
              ),
              text: item.code + '\n',
            },
          ]);
          editor.focus();
        };
        snippetsListContainer.appendChild(el);
      });
    });
  }

  let isResizing = false,
    startX = 0,
    startWidth = 0;
  resizeHandle.addEventListener('mousedown', (e) => {
    if (!isSnippetPanelOpen) return;
    isResizing = true;
    startX = e.clientX;
    startWidth = snippetsPanel.getBoundingClientRect().width;
    resizeHandle.classList.add('dragging');
    document.body.style.cursor = 'col-resize';
    document.body.style.userSelect = 'none';
    e.preventDefault();
  });
  document.addEventListener('mousemove', (e) => {
    if (!isResizing) return;
    const delta = startX - e.clientX;
    let w = startWidth + delta;
    w = Math.max(200, Math.min(600, w));
    snippetsPanel.style.width = w + 'px';
    editor.layout();
  });
  document.addEventListener('mouseup', () => {
    if (!isResizing) return;
    isResizing = false;
    resizeHandle.classList.remove('dragging');
    document.body.style.cursor = '';
    document.body.style.userSelect = '';
    editor.layout();
  });

  const ideModeNode = document.getElementById('ideMode'),
    vimStatusNode = document.getElementById('vimStatus');
  let vimModeInstance = null;
  const vimToggle = document.getElementById('vimToggle');
  vimToggle.addEventListener('change', (e) => {
    if (e.target.checked) {
      ideModeNode.textContent = 'VIM MODE';
      ideModeNode.style.background = '#007acc';
      vimModeInstance = MonacoVim.initVimMode(editor, vimStatusNode);
    } else {
      ideModeNode.textContent = 'STANDARD MODE';
      ideModeNode.style.background = '#424242';
      if (vimModeInstance) {
        vimModeInstance.dispose();
        vimModeInstance = null;
      }
      vimStatusNode.textContent = '';
    }
  });

  editor.onDidChangeCursorPosition((e) => {
    document.getElementById('mouseCoordStatus').textContent =
      `Ln ${e.position.lineNumber}, Col ${e.position.column}`;
  });
  const initPos = editor.getPosition();
  document.getElementById('mouseCoordStatus').textContent =
    `Ln ${initPos.lineNumber}, Col ${initPos.column}`;

  const referenceListView = document.getElementById('referenceListView');
  const referenceDetailView = document.getElementById('referenceDetailView');
  const referenceDetailName = document.getElementById('referenceDetailName');
  const referenceDetailDesc = document.getElementById('referenceDetailDesc');
  const referenceDetailExample = document.getElementById(
    'referenceDetailExample',
  );
  const referenceDetailActions = document.getElementById(
    'referenceDetailActions',
  );

  function showReferenceList() {
    referenceListView.style.display = '';
    referenceDetailView.style.display = 'none';
    referenceModalTitle.textContent = 'Command Reference';
    renderReferenceList(referenceSearch.value);
  }
  let refPreviewEditor = null;

  function showReferenceDetail(item) {
    referenceListView.style.display = 'none';
    referenceDetailView.style.display = '';

    referenceModalTitle.innerHTML = `<div style="width:100%;display:flex;justify-content:space-between;">
    <span>Reference: ${item.name}</span>
    <span id="customRefCloseBtn" style="cursor:pointer;">&times;</span>
  </div>`;
    document.getElementById('customRefCloseBtn').onclick = () => {
      showReferenceList();
    };

    referenceDetailName.textContent = `${item.type}: ${item.name}`;
    referenceDetailDesc.textContent = item.desc;

    if (refPreviewEditor) {
      refPreviewEditor.dispose();
      refPreviewEditor = null;
    }
    referenceDetailExample.innerHTML = '';

    refPreviewEditor = monaco.editor.create(referenceDetailExample, {
      value: item.example || '',
      language: 'duckyscript',
      theme: activeTheme,
      readOnly: true,
      automaticLayout: true,
      fontSize: 13,
      lineNumbers: 'off',
      glyphMargin: false,
      folding: false,
      lineDecorationsWidth: 0,
      lineNumbersMinChars: 0,
      minimap: { enabled: false },
      scrollBeyondLastLine: false,
      renderLineHighlight: 'none',
      selectionHighlight: false,
      occurrencesHighlight: false,
      cursorStyle: 'line',
      cursorBlinking: 'solid',
    });
    setTimeout(() => {
      if (refPreviewEditor) refPreviewEditor.layout();
    }, 100);

    referenceDetailActions.innerHTML = '';
    const insertBtn = document.createElement('button');
    insertBtn.className = 'accent';
    insertBtn.textContent = 'Insert Example';
    insertBtn.onclick = () => {
      const pos = editor.getPosition();
      editor.executeEdits('refDetail', [
        {
          range: new monaco.Range(
            pos.lineNumber,
            pos.column,
            pos.lineNumber,
            pos.column,
          ),
          text: (item.example || '') + '\n',
        },
      ]);
      editor.focus();
    };
    const backBtn = document.createElement('button');
    backBtn.className = 'ghost';
    backBtn.textContent = 'Back to List';
    backBtn.onclick = showReferenceList;
    referenceDetailActions.appendChild(insertBtn);
    referenceDetailActions.appendChild(backBtn);
  }
  const referenceModalTitle = document.getElementById('referenceModalTitle');
  function renderReferenceList(filter = '') {
    referenceListView.innerHTML = '';
    const lower = filter.toLowerCase();
    const filtered = referenceData.filter(
      (i) =>
        i.name.toLowerCase().includes(lower) ||
        i.type.toLowerCase().includes(lower) ||
        i.desc.toLowerCase().includes(lower),
    );
    if (!filtered.length) {
      referenceListView.innerHTML =
        '<div style="color:#aaa;padding:20px;text-align:center;">No matches</div>';
      return;
    }
    filtered.forEach((item) => {
      const el = document.createElement('div');
      el.className = 'template-card';
      el.innerHTML = `<div class="tpl-name">${item.name} <span style="color:#888;font-size:11px;">${item.type}</span></div>
                    <div class="tpl-desc">${item.desc}</div>`;
      el.onclick = () => showReferenceDetail(item);
      referenceListView.appendChild(el);
    });
  }

  document.getElementById('referenceBtn').onclick = () => {
    referenceModal.classList.add('open');
    referenceSearch.value = '';
    showReferenceList();
    setTimeout(() => referenceSearch.focus(), 50);
  };

  const referenceModal = document.getElementById('referenceModal'),
    referenceSearch = document.getElementById('referenceSearch');

  document.getElementById('closeReferenceModal').onclick = () => {
    referenceModal.classList.remove('open');
  };
  referenceModal.onclick = (e) => {
    if (e.target === referenceModal) referenceModal.classList.remove('open');
  };

  referenceSearch.oninput = (e) => {
    if (referenceDetailView.style.display === 'none') {
      renderReferenceList(e.target.value);
    } else {
      showReferenceList();
    }
  };
});
