# Clean Grammar

## Rules
```
START           -> PROGRAM .

PROGRAM         -> MODULE IMPORTS DECLARATIONS .

MODULE          -> T_MODULE T_ID .

IMPORTS         -> IMPORTS IMPORT
                 | .
IMPORT          -> T_IMPORT T_ID T_NEWLINE .

DECLARATIONS    -> DECLARATIONS DECLARATION
                 | DECLARATION .
DECLARATION     -> ENTRY_DECL T_NEWLINE
                 | FUNCTION_DECL T_NEWLINE
                 | INSTANCE_DECL T_NEWLINE
                 | TYPE_DECL T_NEWLINE .

ENTRY_DECL      -> HEADER ENTRY FOOTER
                 | HEADER ENTRY
                 | ENTRY FOOTER
                 | ENTRY .
ENTRY           -> T_START T_ASSIGN EXPRESSION .

FUNCTION_DECL   -> HEADER FUNCTION FOOTER
                 | HEADER FUNCTION
                 | FUNCTION FOOTER
                 | FUNCTION .
FUNCTION        -> T_ID PARAMS CASES T_ASSIGN EXPRESSION .

INSTANCE_DECL   -> INSTANCE FOOTER
                 | INSTANCE .
INSTANCE        -> T_INSTANCE T_REST .

TYPE_DECL       -> T_DOUBLE_COLON T_ID TYPE_PARAMS T_ASSIGN T_REST
                 | T_DOUBLE_COLON T_ID T_ALIAS TYPE CASES .
TYPES           -> TYPES T_COMMA TYPE
                 | TYPE .
TYPE            -> T_INT
                 | T_BOOL
                 | T_ID 
                 | TUPLE_TYPE
                 | LIST_TYPE 
                 | ARRAY_TYPE .

HEADER          -> T_ID T_DOUBLE_COLON TYPE_PARAMS T_RIGHT_ARROW TYPE T_NEWLINE .
FOOTER          -> T_WHERE STATEMENTS .

CASES           -> CASES CASE
                 | .
CASE            -> T_BAR EXPRESSION T_ASSIGN EXPRESSION .

STATEMENTS      -> STATEMENTS STATEMENT
                 | STATEMENT .
STATEMENT       -> T_ID T_ASSIGN EXPRESSION T_NEWLINE .

TUPLE_TYPE      -> T_OPEN TYPES T_CLOSE .
TUPLE           -> T_OPEN TUPLE_VALS T_CLOSE .
TUPLE_VALS      -> TUPLE_VALS T_COMMA EXPRESSION
                 | EXPRESSION T_COMMA EXPRESSION .

LIST_TYPE       -> T_SOPEN TYPE T_SCLOSE .
LIST            -> T_SOPEN T_SCLOSE
                 | T_SOPEN LIST_VALS T_SCLOSE
                 | T_SOPEN LIST_VALS LIST_COLONS T_SCLOSE
                 | T_SOPEN LIST_VALS T_DOT_DOT EXPRESSION T_SCLOSE
                 | T_SOPEN LIST_VALS T_DOT_DOT T_SCLOSE
                 | T_SOPEN LIST_VALS T_LIST_COMP LIST_COMP_FEED LIST_COMP_GUARD T_SCLOSE .
LIST_VALS       -> LIST_VALS T_COMMA EXPRESSION 
                 | EXPRESSION .
LIST_COLONS     -> LIST_COLONS T_COLON EXPRESSION
                 | T_COLON EXPRESSION .
LIST_COMP_FEED  -> LIST_COMP_FEED T_LIST_CONT LIST_COMP_VAL T_LEFT_ARROW T_ID
                 | LIST_COMP_VAL T_LEFT_ARROW T_ID .
LIST_COMP_VAL   -> T_ID
                 | TUPLE .
LIST_COMP_GUARD -> T_BAR EXPRESSION
                 | .

ARRAY_TYPE      -> T_COPEN ARRAY_TYPE_VALS T_CCLOSE .
ARRAY_TYPE_VALS -> ARRAY_TYPE_VALS T_COMMA ARRAY_TYPE_VAL
                 | ARRAY_TYPE_VAL .
ARRAY_TYPE_VAL  -> T_ID T_DOUBLE_COLON TYPE .

ARRAY           -> T_COPEN ARRAY_VALS T_CCLOSE .
ARRAY_VALS      -> ARRAY_VALS T_COMMA ARRAY_VAL
                 | .
ARRAY_VAL       -> T_ID T_ASSIGN EXPRESSION .


TYPE_PARAMS     -> TYPE_PARAMS TYPE
                 | TYPE .
PARAMS          -> PARAMS PARAM
                 | PARAM .
PARAM           -> VALUE
                 | T_OPEN OPERATOR T_CLOSE
                 | T_OPEN T_OPEN LOGIC_OPERATOR T_CLOSE EXPRESSION T_CLOSE T_CLOSE .

FUNCTION_CALL   -> T_ID PARAMS .

EXPRESSION      -> VALUE
                 | FUNCTION_CALL
                 | EXPRESSION OPERATOR VALUE .

VALUE           -> T_ID
                 | TUPLE
                 | LIST
                 | ARRAY
                 | T_STRING
                 | T_CHAR
                 | T_TRUE
                 | T_FALSE
                 | T_NUM
                 | T_OPEN EXPRESSION T_CLOSE .

OPERATOR        -> T_PLUS
                 | T_MINUS
                 | T_MUL
                 | T_DIV
                 | T_POW
                 | T_MOD
                 | T_REM
                 | T_BITOR
                 | T_BITAND
                 | T_BITXOR
                 | T_LIST_CONCAT
                 | T_STRING_CONCAT 
                 | T_INDEX
                 | LOGIC_OPERATOR .

LOGIC_OPERATOR  -> T_EQ
                 | T_NEQ
                 | T_AND
                 | T_OR
                 | T_GT
                 | T_LT
                 | T_GE
                 | T_LE .
```

## Terminals
```
T_MODULE        -> module
T_IMPORT        -> import
T_START         -> Start
T_WHERE         -> where
T_INSTANCE      -> instance
T_BOOL          -> Bool
T_TRUE          -> True
T_FALSE         -> False
T_INT           -> Int
T_REAL          -> Real
T_STRING        -> String
T_CHAR          -> Char
T_COLON         -> :
T_DOUBLE_COLON  -> ::
T_ASSIGN        -> =
T_ALIAS         -> :==
T_RIGHT_ARROW   -> ->
T_LEFT_ARROW    -> <-
T_OPEN          -> (
T_CLOSE         -> )
T_SOPEN         -> [
T_SCLOSE        -> ]
T_COPEN         -> {
T_CCLOSE        -> }
T_COMMA         -> ,
T_UNDERSCORE    -> _
T_BAR           -> |
T_EQ            -> ==
T_NEQ           -> <>
T_GT            -> >
T_LT            -> <
T_GE            -> >=
T_LE            -> <=
T_AND           -> &&
T_OR            -> ||
T_PLUS          -> +
T_MINUS         -> -
T_MUL           -> *
T_DIV           -> /
T_POW           -> ^
T_MOD           -> mod
T_REM           -> rem
T_BITOR         -> bitor
T_BITAND        -> bitand
T_BITXOR        -> bitxor
T_LIST_CONCAT   -> ++
T_STRING_CONCAT -> +++
T_DOT_DOT       -> ..
T_LAMBDA        -> \
T_LIST_COMP     -> \\
T_LIST_CONT     -> &
T_NEGATIVE      -> ~
T_EXCLAMATION   -> !
T_INDEX         -> !!
T_O             -> o
T_NEWLINE       -> \n

T_LINE_COMMENT  -> comment
T_MULTI_COMMENT -> multiline-comment
T_ID            -> id
T_REST          -> rest
T_NUM           -> num
```
