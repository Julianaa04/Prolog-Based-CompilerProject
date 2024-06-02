import tkinter as tk
from enum import Enum
import re
import pandas
import pandastable as pt
from nltk.tree import *


class Token_type(Enum):  # listing all tokens type
    Predicates = 1
    clauses = 2
    goal = 3
    integer = 4
    char = 5
    symbol = 6
    real = 7
    readint = 8
    Semicolon = 9
    EqualOp = 10
    LessThanOp = 11
    GreaterThanOp = 12
    NotEqualOp = 13
    PlusOp = 14
    MinusOp = 15
    MultiplyOp = 16
    DivideOp = 17
    Identifier = 18
    Constant = 19
    Error = 20
    readln = 21
    readchar = 22
    LessThanOrEqualOp = 23
    GreaterThanOrEqualOp = 24
    Dot = 25
    UnderScore = 26
    Comma = 27
    RightParenthesis = 28
    LeftParenthesis = 29
    ColonDash = 30
    Comment = 31
    write = 32
    Number = 33
    Identifier_Variable = 34
    Identifier_Special_Variable = 35
    Identifier_predicate_name = 36
    Invalid_identifier = 37
    Colon = 38
    single_quote = 39
    double_quotes = 40
    string = 41
    single_comment = 42
    begin_multi_comment = 43
    End_multi_comment = 44
    space = 45
    Epsilon = 46
    newline = 47


# class token to hold string and token type
class token:
    def __init__(self, lex, token_type):
        self.lex = lex
        self.token_type = token_type

    def to_dict(self):
        return {
            'Lex': self.lex,
            'token_type': self.token_type
        }


# Reserved word Dictionary
ReservedWords = {"Predicates": Token_type.Predicates,
                 "clauses": Token_type.clauses,
                 "goal": Token_type.goal,
                 "readint": Token_type.readint,
                 "readchar": Token_type.readchar,
                 "readln": Token_type.readln,
                 "write": Token_type.write,
                 "integer": Token_type.integer,
                 "symbol": Token_type.symbol,
                 "string": Token_type.string,
                 "char": Token_type.char,
                 "real": Token_type.real
                 }

ArithmeticOperators = {
    "+": Token_type.PlusOp,
    "-": Token_type.MinusOp,
    "*": Token_type.MultiplyOp,
    "/": Token_type.DivideOp
}

SpecialCharacters = {".": Token_type.Dot,
                     ";": Token_type.Semicolon,
                     #    "_": Token_type.UnderScore,
                     ";": Token_type.Semicolon,
                     ",": Token_type.Comma,
                     "(": Token_type.LeftParenthesis,
                     ")": Token_type.RightParenthesis,
                     ":-": Token_type.ColonDash,
                     ":": Token_type.Colon,
                     # "'":Token_type.single_quote,
                     # '"':Token_type.double_quotes,
                     "%": Token_type.single_comment,
                     "/*": Token_type.begin_multi_comment,
                     "*/": Token_type.End_multi_comment,
                     " ": Token_type.space,
                     "$": Token_type.Epsilon,
                     "/n": Token_type.newline
                     }

RelationalOperators = {"<": Token_type.LessThanOp,
                       "<=": Token_type.LessThanOrEqualOp,
                       ">": Token_type.GreaterThanOp,
                       ">=": Token_type.GreaterThanOrEqualOp,
                       "=": Token_type.EqualOp,
                       "<>": Token_type.NotEqualOp
                       }

Tokens = []  # to add tokens to list
errors = []


# graph(a,5,"ahmed").

def find_token(text):
    token_list = Tokens_Splitting(text)
    for t in token_list:
        if t in ReservedWords:
            Tokens.append(token(t, ReservedWords[t]))

        elif t in ArithmeticOperators:
            Tokens.append(token(t, ArithmeticOperators[t]))

        elif t in RelationalOperators:
            Tokens.append(token(t, RelationalOperators[t]))

        elif t in SpecialCharacters:
            Tokens.append(token(t, SpecialCharacters[t]))

        elif re.match("^[+/-]?[0-9]*$", t):
            Tokens.append(token(t, Token_type.integer))

        elif re.match(r'^[a-z][A-Za-z0-9_]*$', t):
            Tokens.append(token(t, Token_type.Identifier_predicate_name))
        elif re.match(r'^_$', t):
            Tokens.append(token(t, Token_type.Identifier_Special_Variable))

        elif re.match(r'[A-Z_][A-Za-z0-9_]*$', t):
            Tokens.append(token(t, Token_type.Identifier_Variable))

        elif re.match("^[+/-]?[0-9]+(\.[0-9]+)?$", t):
            Tokens.append(token(t, Token_type.real))

        elif re.match(r'"([^"\\]|\\.)*"', t):
            Tokens.append(token(t, Token_type.string))

        elif re.match("^'[^']*'$", t):
            Tokens.append(token(t, Token_type.char))
        elif re.match(r'^[a-z][A-Za-z0-9_]*$', t):
            Tokens.append(token(t, Token_type.symbol))
        else:
            Tokens.append(token(t, Token_type.Error))


def Tokens_Splitting(text):
    x = ""  # holds current token ely wa2fa 3aleh
    List_Tokens = []  # holds list of tokens
    multi_line_comment = False
    single_line_comment = False
    colon_DASHFlag = False
    greaterThanFLag = False
    smallerThanFlag = False

    for i, char in enumerate(text):
        if (not multi_line_comment) and i == 0 and char == '%' and i == text.__len__() - 1:
            List_Tokens.append('%')

        elif (not multi_line_comment) and i == 0 and char == '%':
            single_line_comment = True

        elif (not single_line_comment) and (not multi_line_comment) and i < len(text) - 1 and char == '/' and text[
            i + 1] == '*':
            multi_line_comment = True

        elif multi_line_comment and i < len(text) - 1 and char == '*' and char == '/':
            multi_line_comment = False

        elif single_line_comment or multi_line_comment:
            continue


        elif colon_DASHFlag:
            if x != "":
                List_Tokens.append(x)
                x = ""
            if char == '-':
                List_Tokens.append(":-")
            else:
                List_Tokens.append(":")
                x = x + char
            colon_DASHFlag = False

        elif greaterThanFLag:
            if x != "":
                List_Tokens.append(x)
                x = ""
            if char == '=':
                List_Tokens.append(">=")
                x = ""
            else:
                List_Tokens.append(">")
            greaterThanFLag = False

        elif smallerThanFlag:
            if x != "":
                List_Tokens.append(x)
                x = ""
            if char == '=':
                List_Tokens.append("<=")
            if char == '>':
                List_Tokens.append("<>")
            else:
                List_Tokens.append("<")
            smallerThanFlag = False

        elif char in ReservedWords:
            if x != "":
                List_Tokens.append(x)
                x = ""
            List_Tokens.append(char)

        elif char == ':':
            colon_DASHFlag = True
            continue
        elif char == ">":
            greaterThanFLag = True
        elif char == "<":
            smallerThanFlag = True
        elif char in ArithmeticOperators | RelationalOperators | SpecialCharacters:
            if x != "":
                List_Tokens.append(x)
                x = ""
            List_Tokens.append(char)
        else:
            x = x + char
    if len(x) > 0:
        List_Tokens.append(x)
    return List_Tokens


def Parse():
    j = 0
    Children = []
    Predicate_dict = Predicate(j)
    Children.append(Predicate_dict["node"])
    clause_dict = clause(Predicate_dict["index"])
    Children.append(clause_dict["node"])
    goal_dict = goal(clause_dict["index"])
    Children.append(goal_dict["node"])
    # dic_output = Match(Token_type.Dot, Predicate_dict["index"])
    # Children.append(dic_output["node"])
    Node = Tree('Program', Children)
    return Node


# Predicates graph(string,string$)clauses graph(20$):-A< B+C.goal

def Predicate(j):
    output = dict()
    Children = []
    out = Match(Token_type.Predicates, j)
    Children.append(out["node"])
    out1 = Match(Token_type.space, out["index"])
    Children.append(out1["node"])
    predicateonlyDict = predicateonly(out1["index"])
    Children.append(predicateonlyDict["node"])
    Node = Tree('Predicate', Children)
    output["node"] = Node
    output["index"] = predicateonlyDict["index"]
    return output


def predicateonly(j):
    output = dict()
    Children = []

    if (j < len(Tokens)):
        Temp = Tokens[j + 1].to_dict()

        if (Temp['token_type'] == Token_type.LeftParenthesis):
            out1 = Match(Token_type.Identifier_predicate_name, j)
            Children.append(out1["node"])
            out2 = Match(Token_type.LeftParenthesis, out1["index"])
            Children.append(out2["node"])
            datatype_listDict = datatype_list(out2["index"])
            Children.append(datatype_listDict["node"])
            out3 = Match(Token_type.RightParenthesis, datatype_listDict["index"])
            Children.append(out3["node"])
            Node = Tree('predicateonly', Children)
            output["node"] = Node
            output["index"] = out3["index"]
            return output
        else:
            out3 = Match(Token_type.Identifier_predicate_name, j)
            Children.append(out3["node"])
            Node = Tree('predicateonly', Children)
            output["node"] = Node
            output["index"] = out3["index"]
            return output
    else:
        out4 = Match(Token_type.Epsilon, j)
        Children.append(out4["node"])
        Node = Tree('data', Children)
        output["node"] = Node
        output["index"] = out4["index"]
        return output


def datatype_list(j):
    output = dict()
    Children = []

    datatypeDict = datatype(j)
    Children.append(datatypeDict["node"])
    dataDict = data(datatypeDict["index"])
    Children.append(dataDict["node"])

    Node = Tree('datatype_list', Children)
    output["node"] = Node
    output["index"] = dataDict["index"]
    return output


def datatype(j):
    output = dict()
    Children = []
    if (j < len(Tokens)):
        Temp = Tokens[j].to_dict()
        if (Temp['token_type'] == Token_type.symbol):
            out1 = Match(Token_type.symbol, j)
            Children.append(out1["node"])
            Node = Tree('datatype', Children)
            output["node"] = Node
            output["index"] = out1["index"]
            return output

        elif (Temp['token_type'] == Token_type.string):
            out2 = Match(Token_type.string, j)
            Children.append(out2["node"])
            Node = Tree('datatype', Children)
            output["node"] = Node
            output["index"] = out2["index"]
            return output

        elif (Temp['token_type'] == Token_type.integer):
            out3 = Match(Token_type.integer, j)
            Children.append(out3["node"])
            Node = Tree('datatype', Children)
            output["node"] = Node
            output["index"] = out3["index"]
            return output

        elif (Temp['token_type'] == Token_type.char):
            out4 = Match(Token_type.char, j)
            Children.append(out4["node"])
            Node = Tree('datatype', Children)
            output["node"] = Node
            output["index"] = out4["index"]
            return output

        else:
            out5 = Match(Token_type.real, j)
            Children.append(out5["node"])
            Node = Tree('datatype', Children)
            output["node"] = Node
            output["index"] = out5["index"]
            return output
    else:

        out1 = Match(Token_type.Epsilon, j)
        Children.append(out1["node"])
        Node = Tree('data', Children)
        output["node"] = Node
        output["index"] = j
        return output


def data(j):
    output = dict()
    Children = []
    if (j < len(Tokens)):
        Temp = Tokens[j].to_dict()
        if (Temp['token_type'] == Token_type.Comma):
            out = Match(Token_type.Comma, j)
            Children.append(out["node"])
            datatype_listDict = datatype_list(out["index"])
            Children.append(datatype_listDict["node"])
            Node = Tree('data', Children)
            output["node"] = Node
            output["index"] = datatype_listDict["index"]
            return output

        else:
            out1 = Match(Token_type.Epsilon, j)
            Children.append(out1["node"])
            Node = Tree('data', Children)
            output["node"] = Node
            output["index"] = out1["index"]
            return output
    else:
        out2 = Match(Token_type.Epsilon, j)
        Children.append(out2["node"])
        Node = Tree('data', Children)
        output["node"] = Node
        output["index"] = j
        return output


def clause(j):  # commented function
    output = dict()
    Children = []
    out = Match(Token_type.clauses, j)
    Children.append(out["node"])
    out1 = Match(Token_type.space, out["index"])
    Children.append(out1["node"])
    c_dict = c(out1["index"])
    Children.append(c_dict["node"])
    c_tail_dict = c_tail(c_dict["index"])
    Children.append(c_tail_dict["node"])
    Node = Tree('clause', Children)
    output["node"] = Node
    output["index"] = c_tail_dict["index"]
    return output


def c_tail(j):
    output = dict()
    Children = []
    if j < len(Tokens):
        Temp = Tokens[j].to_dict()
        if (Temp['token_type'] == Token_type.Identifier_predicate_name):
            c_dict = c(j)
            Children.append(c_dict["node"])
            c_tail_dict = c_tail(c_dict["index"])
            Children.append(c_tail_dict["node"])
            Node = Tree('c_tail', Children)
            output["node"] = Node
            output["index"] = c_tail_dict["index"]
            return output
        else:
            Node = Tree('c_tail', Children)
            output["node"] = Node
            output["index"] = j
            return output
    else:
        Node = Tree('c_tail', Children)
        output["node"] = Node
        output["index"] = j
        return output


def c(j):
    output = dict()
    Children = []
    if j < len(Tokens):
        Temp = Tokens[j].to_dict()
        if not isRule(j):
            Facts_dict = Facts(j)
            Children.append(Facts_dict["node"])
            out1 = Match(Token_type.Dot, Facts_dict["index"])
            Children.append(out1["node"])
            Node = Tree('c', Children)
            output["node"] = Node
            output["index"] = out1["index"]
            return output

        elif (Temp['token_type'] == Token_type.Identifier_predicate_name):
            Rule_dict = Rule(j)
            Children.append(Rule_dict["node"])
            out2 = Match(Token_type.Dot, j)
            Children.append(out2["node"])
            Node = Tree('c', Children)
            output["node"] = Node
            output["index"] = Rule_dict["index"]
            return output
        else:
            out2 = Match(Token_type.Epsilon, j)
            Children.append(out2["node"])
            Node = Tree('c', Children)
            output["node"] = Node
            output["index"] = j
            return output

    else:
        out2 = Match(Token_type.Epsilon, j)
        Children.append(out2["node"])
        Node = Tree('c', Children)
        output["node"] = Node
        output["index"] = j
        return output


def isRule(j):
    while j < len(Tokens):
        if Tokens[j].token_type == Token_type.Dot:
            return False
        elif Tokens[j].token_type == Token_type.ColonDash:
            return True
        j += 1


def Rule(j):
    output = dict()
    Children = []
    pred_Dict = pred(j, False)
    Children.append(pred_Dict["node"])
    out1 = Match(Token_type.ColonDash, pred_Dict["index"])
    Children.append(out1["node"])
    Body_dict = Body(out1["index"])
    Children.append(Body_dict["node"])
    Node = Tree('Rule', Children)
    output["node"] = Node
    output["index"] = Body_dict["index"]
    return output


def Facts(j):
    output = dict()
    Children = []
    pred_Dict = pred(j, True)
    Children.append(pred_Dict["node"])
    Node = Tree('Facts', Children)
    output["node"] = Node
    output["index"] = pred_Dict["index"]
    return output


def pred(j, is_fact):
    output = dict()
    Children = []

    if (j < len(Tokens)):
        Temp = Tokens[j + 1].to_dict()

        if (Temp['token_type'] == Token_type.LeftParenthesis):
            out1 = Match(Token_type.Identifier_predicate_name, j)
            Children.append(out1["node"])
            out2 = Match(Token_type.LeftParenthesis, out1["index"])
            Children.append(out2["node"])
            arguments_dict = arguments(out2["index"], is_fact)
            Children.append(arguments_dict["node"])
            out3 = Match(Token_type.RightParenthesis, arguments_dict["index"])
            Children.append(out3["node"])
            Node = Tree('pred', Children)
            output["node"] = Node
            output["index"] = out3["index"]
            return output
        else:
            out3 = Match(Token_type.Identifier_predicate_name, j)
            Children.append(out3["node"])
            Node = Tree('pred', Children)
            output["node"] = Node
            output["index"] = out3["index"]
            return output
    else:
        out4 = Match(Token_type.Epsilon, j)
        Children.append(out4["node"])
        Node = Tree('pred', Children)
        output["node"] = Node
        output["index"] = out4["index"]
        return output


def arguments(j, is_fact):
    output = dict()
    Children = []

    identifier_dict = identifier(j, is_fact)
    Children.append(identifier_dict["node"])
    arg_Dict = arg(identifier_dict["index"], is_fact)
    Children.append(arg_Dict["node"])

    Node = Tree('arguments', Children)
    output["node"] = Node
    output["index"] = arg_Dict["index"]
    return output


def arg(j, is_fact):
    output = dict()
    Children = []
    if (j < len(Tokens)):
        Temp = Tokens[j].to_dict()
        if (Temp['token_type'] == Token_type.Comma):
            out = Match(Token_type.Comma, j)
            Children.append(out["node"])
            arguments_dict = arguments(out["index"], is_fact)
            Children.append(arguments_dict["node"])
            Node = Tree('arg', Children)
            output["node"] = Node
            output["index"] = arguments_dict["index"]
            return output

        else:
            out1 = Match(Token_type.Epsilon, j)
            Children.append(out1["node"])
            Node = Tree('arg', Children)
            output["node"] = Node
            output["index"] = out1["index"]
            return output
    else:
        out2 = Match(Token_type.Epsilon, j)
        Children.append(out2["node"])
        Node = Tree('arg', Children)
        output["node"] = Node
        output["index"] = j
        return output


def identifier(j, is_fact):
    output = dict()
    Children = []
    if (j < len(Tokens)):
        Temp = Tokens[j].to_dict()
        if (Temp['token_type'] == Token_type.Identifier_Variable and is_fact == False):
            out = Match(Token_type.Identifier_Variable, j)
            Children.append(out["node"])
            Node = Tree('identifier', Children)
            output["node"] = Node
            output["index"] = out["index"]
            return output
        else:
            values_dict = values(j)
            Children.append(values_dict["node"])
            Node = Tree('identifier', Children)
            output["node"] = Node
            output["index"] = values_dict["index"]
            return output
    else:
        out2 = Match(Token_type.Epsilon, j)
        Children.append(out2["node"])
        Node = Tree('identifier', Children)
        output["node"] = Node
        output["index"] = j
        return output


def values(j):
    output = dict()
    Children = []
    if (j < len(Tokens)):
        Temp = Tokens[j].to_dict()
        if (Temp['token_type'] == Token_type.Identifier_predicate_name):
            out1 = Match(Token_type.Identifier_predicate_name, j)
            Children.append(out1["node"])
            Node = Tree('values', Children)
            output["node"] = Node
            output["index"] = out1["index"]
            return output

        elif (Temp['token_type'] == Token_type.string):
            out2 = Match(Token_type.string, j)
            Children.append(out2["node"])
            Node = Tree('values', Children)
            output["node"] = Node
            output["index"] = out2["index"]
            return output

        elif (Temp['token_type'] == Token_type.integer):
            out3 = Match(Token_type.integer, j)
            Children.append(out3["node"])
            Node = Tree('values', Children)
            output["node"] = Node
            output["index"] = out3["index"]
            return output

        elif (Temp['token_type'] == Token_type.char):
            out4 = Match(Token_type.char, j)
            Children.append(out4["node"])
            Node = Tree('values', Children)
            output["node"] = Node
            output["index"] = out4["index"]
            return output

        else:
            out5 = Match(Token_type.real, j)
            Children.append(out5["node"])
            Node = Tree('values', Children)
            output["node"] = Node
            output["index"] = out5["index"]
            return output
    else:

        out1 = Match(Token_type.Epsilon, j)
        Children.append(out1["node"])
        Node = Tree('values', Children)
        output["node"] = Node
        output["index"] = j
        return output


# def Head(j):


# def Body_list(j):
#     output = dict()
#     Children = []
#
#     Body_dict = Body(j)
#     Children.append(Body_dict["node"])
#     Body_list_1_dict = Body_list_1(Body_dict["index"])
#     Children.append(Body_list_1_dict["node"])
#
#     Node = Tree('Body_list', Children)
#     output["node"] = Node
#     output["index"] = Body_list_1_dict["index"]
#     return output

# def Body_list_1(j):
#     output = dict()
#     Children = []
#     if (j < len(Tokens)):
#         Temp = Tokens[j].to_dict()
#         if (Temp['token_type'] == Token_type.Comma):
#             out = Match(Token_type.Comma, j)
#             Children.append(out["node"])
#             Body_list_1_dict = Body_list(out["index"])
#             Children.append(Body_list_1_dict["node"])
#             Node = Tree('Body_list_1', Children)
#             output["node"] = Node
#             output["index"] = Body_list_1_dict["index"]
#             return output
#
#         else:
#             out1 = Match(Token_type.Epsilon, j)
#             Children.append(out1["node"])
#             Node = Tree('Body_list_1', Children)
#             output["node"] = Node
#             output["index"] = out1["index"]
#             return output
#     else:
#         out2 = Match(Token_type.Epsilon, j)
#         Children.append(out2["node"])
#         Node = Tree('Body_list_1', Children)
#         output["node"] = Node
#         output["index"] = j
#         return output

def Body(j):
    output = dict()
    Children = []
    Temp = Tokens[j].to_dict()
    # if (Temp['token_type'] == Token_type.readint or Temp['token_type'] == Token_type.readchar or Temp['token_type'] == Token_type.readln or Temp['token_type'] == Token_type.write):
    #     Builtin_dict = Builtin(j)
    #     Children.append(Builtin_dict["node"])
    #     Node = Tree('Body', Children)
    #     output["node"] = Node

    #     output["index"] = Builtin_dict["index"]
    #     return output
    # if (Temp['token_type'] == Token_type.Identifier_predicate_name):
    X = Tokens[j + 1].to_dict()
    if (X['token_type'] == Token_type.PlusOp or Temp['token_type'] == Token_type.MinusOp or
            Temp['token_type'] == Token_type.MultiplyOp or Temp['token_type'] == Token_type.DivideOp):
        Expression_Dict = Expression(j)
        Children.append(Expression_Dict["node"])
        Node = Tree('Body', Children)
        output["node"] = Node
        output["index"] = Expression_Dict["index"]
        return output
    else:
        Relational_Dict = V_Expression(j)
        Children.append(Relational_Dict["node"])
        Node = Tree('Body', Children)
        output["node"] = Node
        output["index"] = Relational_Dict["index"]
        return output
        # Relational_Dict = RelationalOperators2(j)
        # Children.append(Relational_Dict["node"])
        # Node = Tree('Body', Children)
        # output["node"] = Node
        # output["index"] = Relational_Dict["index"]
        # return output

    # else:
    #     # Comment_Dict = Comment(j)
    #     # Children.append(Comment_Dict["node"])
    #     Node = Tree('Body', Children)
    #     output["node"] = Node
    #     output["index"] = j
    #     # output["index"] = Comment_Dict["index"]
    #     return output


def Builtin(j):
    output = dict()
    Children = []
    if (j < len(Tokens)):
        Temp = Tokens[j].to_dict()
        if (Temp['token_type'] == Token_type.readint):
            out = Match(Token_type.readint, j)
            Children.append(out["node"])
            out1 = Match(Token_type.LeftParenthesis, out["index"])
            Children.append(out1["node"])
            out2 = Match(Token_type.Identifier_Variable, j)
            Children.append(out2["node"])
            out3 = Match(Token_type.RightParenthesis, out2["index"])
            Children.append(out3["node"])
            Node = Tree('Builtin', Children)
            output["node"] = Node
            output["index"] = out3["index"]
            return output
        elif (Temp['token_type'] == Token_type.readchar):
            out4 = Match(Token_type.readchar, j)
            Children.append(out4["node"])
            out5 = Match(Token_type.LeftParenthesis, out4["index"])
            Children.append(out5["node"])
            out6 = Match(Token_type.Identifier_Variable, j)
            Children.append(out6["node"])
            out7 = Match(Token_type.RightParenthesis, out6["index"])
            Children.append(out7["node"])
            Node = Tree('Builtin', Children)
            output["node"] = Node
            output["index"] = out7["index"]
            return output
        elif (Temp['token_type'] == Token_type.readln):
            out8 = Match(Token_type.readln, j)
            Children.append(out8["node"])
            out9 = Match(Token_type.LeftParenthesis, out8["index"])
            Children.append(out9["node"])
            out10 = Match(Token_type.Identifier_Variable, j)
            Children.append(out10["node"])
            out11 = Match(Token_type.RightParenthesis, out10["index"])
            Children.append(out11["node"])
            Node = Tree('Builtin', Children)
            output["node"] = Node
            output["index"] = out11["index"]
            return output
        elif (Temp['token_type'] == Token_type.write):
            out12 = Match(Token_type.write, j)
            Children.append(out12["node"])
            out13 = Match(Token_type.LeftParenthesis, out12["index"])
            Children.append(out13["node"])
            out14 = Match(Token_type.double_quotes, out13["index"])
            Children.append(out14["node"])
            op_dict = op(out14["index"])
            Children.append(op_dict["node"])
            out15 = Match(Token_type.double_quotes, op_dict["index"])
            Children.append(out15["node"])
            Node = Tree('Builtin', Children)
            output["node"] = Node
            output["index"] = out15["index"]
            return output
        else:
            out16 = Match(Token_type.Epsilon, j)
            Children.append(out16["node"])
            Node = Tree('Builtin', Children)
            output["node"] = Node
            output["index"] = out16["index"]
            return output

    else:
        out17 = Match(Token_type.Epsilon, j)
        Children.append(out17["node"])
        Node = Tree('Builtin', Children)
        output["node"] = Node
        output["index"] = j
        return output


# def op(j):
#     output = dict()
#     Children = []
#     pro_dict = pro(j)
#     Children.append(pro_dict["node"])
#     op_dict = op(j)
#     Children.append(op_dict["node"])
#     Node = Tree('op', Children)
#     output["node"] = Node
#     output["index"] = op_dict["index"]
#     return output

#
# def Number(j):
#     output = dict()
#     Children = []
#     if (j < len(Tokens)):
#         Temp = Tokens[j].to_dict()
#         if (Temp['token_type'] == Token_type.integer):
#             out1 = Match(Token_type.integer, j)
#             Children.append(out1["node"])
#             Node = Tree('Number', Children)
#             output["node"] = Node
#             output["index"] = out1["index"]
#             return output
#
#         else:
#             out2 = Match(Token_type.real, j)
#             Children.append(out2["node"])
#             Node = Tree('Number', Children)
#             output["node"] = Node
#             output["index"] = out2["index"]
#             return output
#     else:
#         out1 = Match(Token_type.Epsilon, j)
#         Children.append(out1["node"])
#         Node = Tree('Number', Children)
#         output["node"] = Node
#         output["index"] = j
#         return output
#
#
# def pro(j):
#     output = dict()
#     Children = []
#     Temp = Tokens[j].to_dict()
#     if (Temp['token_type'] == Token_type.Predicates or Temp['token_type'] == Token_type.clauses or
#             Temp['token_type'] == Token_type.goal or Temp['token_type'] == Token_type.readint or
#             Temp['token_type'] == Token_type.readchar or Temp['token_type'] == Token_type.readln or
#             Temp['token_type'] == Token_type.write or Temp['token_type'] == Token_type.string or
#             Temp['token_type'] == Token_type.integer or Temp['token_type'] == Token_type.symbol or
#             Temp['token_type'] == Token_type.char or Temp['token_type'] == Token_type.real):
#         ReservedWords_Dict = ReservedWords
#         Children.append(ReservedWords_Dict["node"])
#         Node = Tree('pro', Children)
#         output["node"] = Node
#         output["index"] = ReservedWords_Dict["index"]
#         return output
#
#     elif (Temp['token_type'] == Token_type.PlusOp or Temp['token_type'] == Token_type.MinusOp or
#           Temp['token_type'] == Token_type.MultiplyOp or Temp['token_type'] == Token_type.DivideOp):
#         ArithmeticOperators_Dict = ArithmeticOperators
#         Children.append(ArithmeticOperators_Dict["node"])
#         Node = Tree('pro', Children)
#         output["node"] = Node
#         output["index"] = ArithmeticOperators_Dict["index"]
#         return output
#
#     elif (Temp['token_type'] == Token_type.LessThanOp or Temp['token_type'] == Token_type.GreaterThanOp or
#           Temp['token_type'] == Token_type.EqualOp or Temp['token_type'] == Token_type.GreaterThanOrEqualOp or
#           Temp['token_type'] == Token_type.LessThanOrEqualOp or Temp['token_type'] == Token_type.NotEqualOp):
#         RelationalOperators_Dict = RelationalOperators
#         Children.append(RelationalOperators_Dict["node"])
#         Node = Tree('pro', Children)
#         output["node"] = Node
#         output["index"] = RelationalOperators_Dict["index"]
#         return output
#
#     elif (Temp['token_type'] == Token_type.Dot or Temp['token_type'] == Token_type.Semicolon or
#           Temp['token_type'] == Token_type.Comma or Temp['token_type'] == Token_type.LeftParenthesis or
#           Temp['token_type'] == Token_type.RightParenthesis or Temp['token_type'] == Token_type.Colon or
#           Temp['token_type'] == Token_type.ColonDash or Temp['token_type'] == Token_type.single_comment or
#           Temp['token_type'] == Token_type.begin_multi_comment or Temp['token_type'] == Token_type.End_multi_comment or
#           Temp['token_type'] == Token_type.single_quote or Temp['token_type'] == Token_type.double_quotes):
#         SpecialCharacters_Dict = SpecialCharacters
#         Children.append(SpecialCharacters_Dict["node"])
#         Node = Tree('pro', Children)
#         output["node"] = Node
#         output["index"] = SpecialCharacters_Dict["index"]
#         return output
#
#     elif (Temp['token_type'] == Token_type.Dot or Temp['token_type'] == Token_type.Semicolon or
#           Temp['token_type'] == Token_type.Comma or Temp['token_type'] == Token_type.LeftParenthesis or
#           Temp['token_type'] == Token_type.RightParenthesis or Temp['token_type'] == Token_type.Colon or
#           Temp['token_type'] == Token_type.ColonDash or Temp['token_type'] == Token_type.single_comment or
#           Temp['token_type'] == Token_type.begin_multi_comment or Temp['token_type'] == Token_type.End_multi_comment or
#           Temp['token_type'] == Token_type.single_quote or Temp['token_type'] == Token_type.double_quotes):
#         SpecialCharacters_Dict = SpecialCharacters
#         Children.append(SpecialCharacters_Dict["node"])
#
#
#     elif (Temp['token_type'] == Token_type.Identifier_Variable):
#         out5 = Match(Token_type.Identifier_Variable, j)
#         Children.append(out5["node"])
#         Node = Tree('pro', Children)
#         output["node"] = Node
#         output["index"] = out5["index"]
#         return output
#     else:
#
#         Node = Tree('pro', Children)
#         output["node"] = Node
#         output["index"] = j
#         return output

# def Expression(j):
#     output = dict()
#     Children = []
#     Temp = Tokens[j].to_dict()
#     if(Temp['token_type'] == Token_type.Identifier_Variable):
#         out = Match(Token_type.Identifier_Variable, j)
#         Children.append(out["node"])

#     elif(Temp['token_type'] == Token_type.PlusOp or Temp['token_type'] == Token_type.MinusOp or Temp['token_type'] == Token_type.MultiplyOp or Temp['token_type'] == Token_type.DivideOp ):
#          ArithmeticOperators_Dict = ArithmeticOperators_(out["index"])
#          Children.append(ArithmeticOperators_Dict["node"])
#          Ex_Dict = Ex(out["index"])
#          Children.append(Ex_Dict["node"])
#          Node = Tree('Expression', Children)
#          output["node"] = Node
#          output["index"] = Ex_Dict["index"]
#          return output
#     else:
#         Node = Tree('Expression', Children)
#         output["node"] = Node
#         output["index"] =j
#         return output


def Expression(j):
    output = dict()
    Children = []
    out = Match(Token_type.Identifier_Variable, j)
    Children.append(out["node"])
    ArithmeticOperators_Dict = ArithmeticOperators_(out["index"])
    Children.append(ArithmeticOperators_Dict["node"])
    Ex_Dict = Ex(out["index"])
    Children.append(Ex_Dict["node"])
    Node = Tree('Expression', Children)
    output["node"] = Node
    output["index"] = Ex_Dict["index"]
    return output


def ArithmeticOperators_(j):
    output = dict()
    Children = []

    Temp = Tokens[j].to_dict()
    # out = Match(Token_type.PlusOp, j)
    # Children.append(out["node"])
    # Node = Tree('ArithmeticOperators', Children)
    # output["node"] = Node
    # output["index"] = out["index"]
    # return output
    if Temp['token_type'] == Token_type.PlusOp:
        out = Match(Token_type.PlusOp, j)
        Children.append(out["node"])
        Node = Tree('ArithmeticOperators', Children)
        output["node"] = Node
        output["index"] = out["index"]
        return output

        #     elif (Temp['token_type'] == Token_type.MinusOp):
    #         out1 = Match(Token_type.MinusOp, j)
    #         Children.append(out1["node"])
    #         Node = Tree('ArithmeticOperators', Children)
    #         output["node"] = Node
    #         output["index"] = out1["index"]
    #         return output
    #     elif (Temp['token_type'] == Token_type.MultiplyOp):
    #         out2 = Match(Token_type.MultiplyOp,j)
    #         Children.append(out2["node"])
    #         Node = Tree('ArithmeticOperators', Children)
    #         output["node"] = Node
    #         output["index"] = out2["index"]
    #         return output
    #     elif(Temp['token_type'] == Token_type.DivideOp):
    #         out3 = Match(Token_type.DivideOp,j)
    #         Children.append(out3["node"])
    #         Node = Tree('ArithmeticOperators', Children)
    #         output["node"] = Node
    #         output["index"] = out3["index"]
    #         return output
    else:
        Node = Tree('ArithmeticOperators', Children)
        output["node"] = Node
        output["index"] = j
        return output


def RelationalOperators2(j):
    output = dict()
    Children = []

    #  Temp = Tokens[j].to_dict()

    #  if(Temp['token_type']==Token_type.GreaterThanOp):
    #      out = Match(Token_type.GreaterThanOp,j)
    #      Children.append(out["node"])
    #      Node = Tree('RelationalOperators2', Children)
    #      output["node"] = Node
    #      output["index"] = out["index"]
    #      return output
    #  elif(Temp['token_type']==Token_type.LessThanOp):
    out1 = Match(Token_type.LessThanOp, j)
    Children.append(out1["node"])
    Node = Tree('RelationalOperators2', Children)
    output["node"] = Node
    output["index"] = out1["index"]
    return output


#  elif(Temp['token_type']==Token_type.GreaterThanOrEqualOp):
#      out2 = Match(Token_type.GreaterThanOrEqualOp, j)
#      Children.append(out2["node"])
#      Node = Tree('RelationalOperators2', Children)
#      output["node"] = Node
#      output["index"] = out2["index"]
#      return output
#  elif(Temp['token_type']==Token_type.LessThanOrEqualOp):
#      out3 = Match(Token_type.LessThanOrEqualOp, j)
#      Children.append(out3["node"])
#      Node = Tree('RelationalOperators2', Children)
#      output["node"] = Node
#      output["index"] = out3["index"]
#      return output
#  else:
#      out4 = Match(Token_type.NotEqualOp, j)
#      Children.append(out4["node"])
#      Node = Tree('RelationalOperators2', Children)
#      output["node"] = Node
#      output["index"] = out4["index"]
#      return output


def Ex(j):
    output = dict()
    Children = []
    Temp = Tokens[j].to_dict()
    if (Temp['token_type'] == Token_type.Identifier_Variable or Temp['token_type'] == Token_type.integer or Temp[
        'token_type'] == Token_type.real):

        TypeExpression_dict = TypeExpression(j)
        Children.append(TypeExpression_dict["node"])
        Node = Tree('Ex', Children)
        output["node"] = Node
        output["index"] = TypeExpression_dict["index"]
        return output

    else:
        Expression_dict = Expression(j)
        Children.append(Expression_dict["node"])
        Node = Tree('Ex', Children)
        output["node"] = Node
        output["index"] = Expression_dict["index"]
        return output


# def Ex(j):
#     output = dict()
#     Children = []
#     Temp = Tokens[j+1].to_dict()
#     if(Temp['token_type'] == Token_type.PlusOp or Temp['token_type'] == Token_type.MinusOp or Temp['token_type'] == Token_type.MultiplyOp or Temp['token_type'] == Token_type.DivideOp ):

#             Expression_dict = Expression(j)
#             Children.append(Expression_dict["node"])
#             Node = Tree('Ex', Children)
#             output["node"] = Node
#             output["index"] = Expression_dict["index"]
#             return output

#     else:
#             TypeExpression_dict = TypeExpression(j)
#             Children.append(TypeExpression_dict["node"])
#             Node = Tree('Ex', Children)
#             output["node"] = Node
#             output["index"] = TypeExpression_dict["index"]
#             return output


def TypeExpression(j):
    output = dict()
    Children = []
    if (j < len(Tokens)):
        Temp = Tokens[j].to_dict()
        if (Temp['token_type'] == Token_type.Identifier_Variable):
            out1 = Match(Token_type.Identifier_Variable, j)
            Children.append(out1["node"])
            Node = Tree('TypeExpression', Children)
            output["node"] = Node
            output["index"] = out1["index"]
            return output

        elif (Temp['token_type'] == Token_type.integer):
            out2 = Match(Token_type.integer, j)
            Children.append(out2["node"])
            Node = Tree('TypeExpression', Children)
            output["node"] = Node
            output["index"] = out2["index"]
            return output

        elif (Temp['token_type'] == Token_type.real):
            out3 = Match(Token_type.real, j)
            Children.append(out3["node"])
            Node = Tree('TypeExpression', Children)
            output["node"] = Node
            output["index"] = out3["index"]
            return output
        else:
            Node = Tree('TypeExpression', Children)
            output["node"] = Node
            output["index"] = j
            return output
    else:
        Node = Tree('TypeExpression', Children)
        output["node"] = Node
        output["index"] = j
        return output


def V_Expression(j):
    output = dict()
    Children = []
    out = Match(Token_type.Identifier_Variable, j)
    Children.append(out["node"])
    RelationalOperators_Dict = RelationalOperators2(out["index"])
    Children.append(RelationalOperators_Dict["node"])
    Z_Expression_Dict = Z_Expression(RelationalOperators_Dict["index"])
    Children.append(Z_Expression_Dict["node"])
    Node = Tree('V_Expression', Children)
    output["node"] = Node
    output["index"] = Z_Expression_Dict["index"]
    return output


# def Z_Expression(j):
#     output = dict()
#     Children = []
#     Temp = Tokens[j].to_dict()
#     if(Temp['token_type'] == Token_type.Identifier_Variable or Temp['token_type'] == Token_type.integer or Temp['token_type'] == Token_type.real):

#             TypeExpression_dict = TypeExpression(j)
#             Children.append(TypeExpression_dict["node"])
#             Node = Tree('Ex', Children)
#             output["node"] = Node
#             output["index"] = TypeExpression_dict["index"]
#             return output

#     else:
#             Expression_dict = Expression(j)
#             Children.append(Expression_dict["node"])
#             Node = Tree('Ex', Children)
#             output["node"] = Node
#             output["index"] = Expression_dict["index"]
#             return output
def Z_Expression(j):
    output = dict()
    Children = []
    # Temp = Tokens[j].to_dict()
    # if (Temp['token_type']==Token_type.GreaterThanOp or Temp['token_type']==Token_type.LessThanOp or Temp['token_type']==Token_type.GreaterThanOrEqualOp or Temp['token_type']==Token_type.LessThanOrEqualOp):

    Expression_dict = Expression(j)
    Children.append(Expression_dict["node"])
    Node = Tree('Z_Expression', Children)
    output["node"] = Node
    output["index"] = Expression_dict["index"]
    return output

    # else:
    #     TypeExpression_dict = TypeExpression(j)
    #     Children.append(TypeExpression_dict["node"])
    #     Node = Tree('Z_Expression', Children)
    #     output["node"] = Node
    #     output["index"] = TypeExpression_dict["index"]
    #     return output


def Comment(j):
    output = dict()
    Children = []
    if (j < len(Tokens)):
        Temp = Tokens[j].to_dict()
        if (Temp['token_type'] == Token_type.single_comment):
            out = Match(Token_type.single_comment, j)
            Children.append(out["node"])
            op_dict = op(out["index"])
            Children.append(op_dict["node"])
            Node = Tree('Comment', Children)
            output["node"] = Node
            output["index"] = op_dict["index"]
            return output
        else:
            out1 = Match(Token_type.begin_multi_comment, j)
            Children.append(out1["node"])
            op_dict = op(out1["index"])
            Children.append(op_dict["node"])
            out2 = Match(Token_type.End_multi_comment, op_dict["index"])
            Children.append(out2["node"])
            Node = Tree('Comment', Children)
            output["node"] = Node
            output["index"] = out2["index"]
            return output
    else:
        Node = Tree('Comment', Children)
        output["node"] = Node
        output["index"] = j
        return output


def op(j):
    output = dict()
    Children = []
    if (j < len(Tokens)):
        Temp = Tokens[j].to_dict()
        if (Temp['token_type'] == Token_type.Identifier_Variable):
            out1 = Match(Token_type.Identifier_Variable, j)
            Children.append(out1["node"])
            pros_Dict = pros(out1["index"])
            Children.append(pros_Dict["node"])
            Node = Tree('op', Children)
            output["node"] = Node
            output["index"] = pros_Dict["index"]
            return output

        elif (Temp['token_type'] == Token_type.Identifier_predicate_name):
            out2 = Match(Token_type.Identifier_predicate_name, j)
            Children.append(out2["node"])
            pros_Dict = pros(out2["index"])
            Children.append(pros_Dict["node"])
            Node = Tree('op', Children)
            output["node"] = Node
            output["index"] = pros_Dict["index"]
            return output

        elif (Temp['token_type'] == Token_type.PlusOp or Temp['token_type'] == Token_type.MinusOp or
              Temp['token_type'] == Token_type.MultiplyOp or Temp['token_type'] == Token_type.DivideOp):
            ArithmeticOperators_Dict = ArithmeticOperators
            Children.append(ArithmeticOperators_Dict["node"])
            pros_Dict = pros(ArithmeticOperators_Dict["index"])
            Children.append(pros_Dict["node"])
            Node = Tree('op', Children)
            output["node"] = Node
            output["index"] = pros_Dict["index"]
            return output

        elif (Temp['token_type'] == Token_type.LessThanOp or Temp['token_type'] == Token_type.GreaterThanOp or
              Temp['token_type'] == Token_type.EqualOp or Temp['token_type'] == Token_type.GreaterThanOrEqualOp or
              Temp['token_type'] == Token_type.LessThanOrEqualOp or Temp['token_type'] == Token_type.NotEqualOp):
            RelationalOperators_Dict = RelationalOperators
            Children.append(RelationalOperators_Dict["node"])
            pros_Dict = pros(RelationalOperators_Dict["index"])
            Children.append(pros_Dict["node"])
            Node = Tree('op', Children)
            output["node"] = Node
            output["index"] = pros_Dict["index"]
            return output
        elif (Temp['token_type'] == Token_type.Dot or Temp['token_type'] == Token_type.Semicolon or
              Temp['token_type'] == Token_type.Comma or Temp['token_type'] == Token_type.LeftParenthesis or
              Temp['token_type'] == Token_type.RightParenthesis or Temp['token_type'] == Token_type.Colon or
              Temp['token_type'] == Token_type.ColonDash or Temp['token_type'] == Token_type.single_comment or
              Temp['token_type'] == Token_type.begin_multi_comment or Temp[
                  'token_type'] == Token_type.End_multi_comment or
              Temp['token_type'] == Token_type.single_quote or Temp['token_type'] == Token_type.double_quotes):
            SpecialCharacters_Dict = SpecialCharacters
            Children.append(SpecialCharacters_Dict["node"])
            pros_Dict = pros(SpecialCharacters_Dict["index"])
            Children.append(pros_Dict["node"])
            Node = Tree('op', Children)
            output["node"] = Node
            output["index"] = pros_Dict["index"]
            return output
    else:
        out1 = Match(Token_type.Epsilon, j)
        Children.append(out1["node"])
        Node = Tree('op', Children)
        output["node"] = Node
        output["index"] = j
        return output


def pros(j):
    output = dict()
    Children = []
    if (j < len(Tokens)):
        Temp = Tokens[j].to_dict()
        if (Temp['token_type'] == Token_type.newline):
            out = Match(Token_type.newline, j)
            Children.append(out["node"])
            op_dict = op(out["index"])
            Children.append(op_dict["node"])
            Node = Tree('pros', Children)
            output["node"] = Node
            output["index"] = j
            return output

        else:
            out1 = Match(Token_type.Epsilon, j)
            Children.append(out1["node"])
            Node = Tree('pros', Children)
            output["node"] = Node
            output["index"] = out1["index"]
            return output
    else:
        out2 = Match(Token_type.Epsilon, j)
        Children.append(out2["node"])
        Node = Tree('arg', Children)
        output["node"] = Node
        output["index"] = j
        return output


def Goal(j):
    output = dict()
    Children = []
    out = Match(Token_type.goal, j)
    Children.append(out["node"])
    out1 = Match(Token_type.space, out["index"])
    Children.append(out1["node"])
    goal_Dict = goal(out1["index"])
    Children.append(goal_Dict["node"])
    Node = Tree('Goal', Children)
    output["node"] = Node
    output["index"] = goal_Dict["index"]
    return output


def goal(j):
    output = dict()
    Children = []

    if (j < len(Tokens)):
        Temp = Tokens[j + 1].to_dict()

        if (Temp['token_type'] == Token_type.LeftParenthesis):
            out1 = Match(Token_type.Identifier_predicate_name, j)
            Children.append(out1["node"])
            out2 = Match(Token_type.LeftParenthesis, out1["index"])
            Children.append(out2["node"])
            arguments_Dict = arguments(out2["index"])
            Children.append(arguments_Dict["node"])
            out3 = Match(Token_type.RightParenthesis, arguments_Dict["index"])
            Children.append(out3["node"])
            Node = Tree('goal', Children)
            output["node"] = Node
            output["index"] = out3["index"]
            return output
        else:
            out4 = Match(Token_type.Identifier_predicate_name, j)
            Children.append(out4["node"])
            Node = Tree('goal', Children)
            output["node"] = Node
            output["index"] = out4["index"]
            return output
    else:
        out5 = Match(Token_type.Epsilon, j)
        Children.append(out5["node"])
        Node = Tree('goal', Children)
        output["node"] = Node
        output["index"] = out5["index"]
        return output


#
# def Relation(j):
#     output = dict()
#     Children = []
#
#     Rexp_dict = Rexp(j)
#     Children.append(Rexp_dict["node"])
#     Expression_dict = Expression(Rexp_dict["index"])
#     Children.append(Expression_dict["node"])
#
#     Node = Tree('Relation', Children)
#     output["node"] = Node
#     output["index"] = Expression_dict["index"]
#     return output
#
# def Rexp(j):
#     output = dict()
#     Children = []
#     Expression_dict = Expression(j)
#     Children.append(Expression_dict["node"])
#     Rex_dict = Rex(Expression_dict["index"])
#     Children.append(Rex_dict["node"])
#
#     Node = Tree('Rexp', Children)
#     output["node"] = Node
#     output["index"] = Rex_dict["index"]
#     return output
#
# def Rex(j):
#     output = dict()
#     Children = []
#     if (j < len(Tokens)):
#         Temp = Tokens[j].to_dict()
#         if(Temp['token_type'] ==Token_type.LessThanOrEqualOp):
#             out = Match(Token_type.LessThanOrEqualOp, j)
#             Children.append(out["node"])
#             Node = Tree('Rex', Children)
#             output["node"] = Node
#             output["index"] = out["index"]
#             return output
#         elif(Temp['token_type'] == Token_type.GreaterThanOrEqualOp):
#             out1 = Match(Token_type.GreaterThanOrEqualOp, j)
#             Children.append(out1["node"])
#             Node = Tree('Rex', Children)
#             output["node"] = Node
#             output["index"] = out1["index"]
#             return output
#         elif(Temp['token_type'] == Token_type.LessThanOp):
#             out2 = Match(Token_type.Token_type.LessThanOp, j)
#             Children.append(out2["node"])
#             Node = Tree('Rex', Children)
#             output["node"] = Node
#             output["index"] = out2["index"]
#             return output
#         elif (Temp['token_type'] == Token_type.GreaterThanOp):
#             out3 = Match(Token_type.Token_type.GreaterThanOp, j)
#             Children.append(out3["node"])
#             Node = Tree('Rex', Children)
#             output["node"] = Node
#             output["index"] = out3["index"]
#             return output
#         elif (Temp['token_type'] == Token_type.EqualOp):
#             out4 = Match(Token_type.Token_type.EqualOp, j)
#             Children.append(out4["node"])
#             Node = Tree('Rex', Children)
#             output["node"] = Node
#             output["index"] = out4["index"]
#             return output
#
#     else:
#
#         out5 = Match(Token_type.Epsilon, j)
#         Children.append(out5["node"])
#         Node = Tree('Rex', Children)
#         output["node"] = Node
#         output["index"] = j
#         return output
#
#
#
# def Expression(j):
#     output = dict()
#     Children = []
#
#     Term_dict = Term(j)
#     Children.append(Term_dict["node"])
#     Exp_dict = Exp(Term_dict["index"])
#     Children.append(Exp_dict["node"])
#
#     Node = Tree('Expression', Children)
#     output["node"] = Node
#     output["index"] = Exp_dict["index"]
#     return output
#
# def Exp(j):
#     output = dict()
#     Children = []
#     if (j < len(Tokens)):
#         Temp = Tokens[j].to_dict()
#         if (Temp['token_type'] == Token_type.PlusOp):
#             out = Match(Token_type.PlusOp, j)
#             Children.append(out["node"])
#             Term_Dict = Term(out["index"])
#             Children.append(Term_Dict["node"])
#             Exp_dict = Exp(out["index"])
#             Children.append(Exp_dict["node"])
#             Node = Tree('Exp', Children)
#             output["node"] = Node
#             output["index"] = Exp_dict["index"]
#             return output
#
#         elif (Temp['token_type'] == Token_type.MinusOp):
#             out1 = Match(Token_type.MinusOp, j)
#             Children.append(out1["node"])
#             Term_Dict = Term(out1["index"])
#             Children.append(Term_Dict["node"])
#             Exp_dict = Exp(out1["index"])
#             Children.append(Exp_dict["node"])
#             Node = Tree('Exp', Children)
#             output["node"] = Node
#             output["index"] = Exp_dict["index"]
#             return output
#         else:
#             out2 = Match(Token_type.Epsilon, j)
#             Children.append(out2["node"])
#             Node = Tree('Exp', Children)
#             output["node"] = Node
#             output["index"] = out2["index"]
#             return output
#
#     else:
#         out3 = Match(Token_type.Epsilon, j)
#         Children.append(out3["node"])
#         Node = Tree('Exp', Children)
#         output["node"] = Node
#         output["index"] = j
#         return output
#
#
#
# def predicate_list(j):
#     output = dict()
#     Children = []
#
#     pred_Dict= pred(j)
#     Children.append(pred_Dict["node"])
#     pre_Dict = pre(pred_Dict["index"])
#     Children.append(pre_Dict["node"])
#
#     Node = Tree('predicate_list', Children)
#     output["node"] = Node
#     output["index"] = pre_Dict["index"]
#     return output
#
# def pre(j):
#     output = dict()
#     Children = []
#     if (j < len(Tokens)):
#         Temp = Tokens[j].to_dict()
#         if (Temp['token_type'] == Token_type.Comma):
#             out = Match(Token_type.Comma, j)
#             Children.append(out["node"])
#             predicate_list_Dict = predicate_list(out["index"])
#             Children.append(predicate_list_Dict["node"])
#             Node = Tree('pre', Children)
#             output["node"] = Node
#             output["index"] = predicate_list_Dict["index"]
#             return output
#         elif (Temp['token_type'] == Token_type.Semicolon):
#             out1 = Match(Token_type.Comma, j)
#             Children.append(out1["node"])
#             predicate_list_Dict = predicate_list(out1["index"])
#             Children.append(predicate_list_Dict["node"])
#             Node = Tree('pre', Children)
#             output["node"] = Node
#             output["index"] = predicate_list_Dict["index"]
#             return output
#         else:
#             out2 = Match(Token_type.Epsilon, j)
#             Children.append(out2["node"])
#             Node = Tree('pre', Children)
#             output["node"] = Node
#             output["index"] = out2["index"]
#             return output
#
#     else:
#         out3 = Match(Token_type.Epsilon, j)
#         Children.append(out3["node"])
#         Node = Tree('pre', Children)
#         output["node"] = Node
#         output["index"] = j
#         return output


# def Header(j):
#      Children = []
#      out = dict()
#      out_pro1 = Match(Token_type.Program, j)
#      Children.append(out_pro1["node"])
#      out_pro2 = Match(Token_type.Identifier, out_pro1["index"])
#      Children.append(out_pro2["node"])
#      out_pro3 = Match(Token_type.Semicolon, out_pro2["index"])
#      Children.append(out_pro3["node"])
#      Node = Tree('Header', Children)
#      out["node"] = Node
#      out["index"] = out_pro3["index"]
#      return out
#
#
# 'Header'

def Match(a, j):
    output = dict()
    if (j < len(Tokens)):
        Temp = Tokens[j].to_dict()
        if (Temp['token_type'] == a):
            j += 1
            output["node"] = [Temp['Lex']]
            output["index"] = j
            return output
        else:
            output["node"] = ["error"]
            output["index"] = j + 1
            errors.append("Syntax error : " + Temp['Lex'] + " Expected dot")
            return output
    else:
        output["node"] = ["error"]
        output["index"] = j + 1
        return output


# GUI
root = tk.Tk()

canvas1 = tk.Canvas(root, width=400, height=300, relief='raised')
canvas1.pack()

label1 = tk.Label(root, text='Scanner Phase')
label1.config(font=('helvetica', 14))
canvas1.create_window(200, 25, window=label1)

label2 = tk.Label(root, text='Source code:')
label2.config(font=('helvetica', 10))
canvas1.create_window(200, 100, window=label2)

entry1 = tk.Entry(root)
canvas1.create_window(200, 140, window=entry1)


def Scan():
    x1 = entry1.get()
    find_token(x1)
    df = pandas.DataFrame.from_records([t.to_dict() for t in Tokens])
    # print(df)

    # to display token stream as table
    dTDa1 = tk.Toplevel()
    dTDa1.title('Token Stream')
    dTDaPT = pt.Table(dTDa1, dataframe=df, showtoolbar=True, showstatusbar=True)
    dTDaPT.show()
    # start Parsing
    Node = Parse()

    # to display errorlist
    df1 = pandas.DataFrame(errors)
    dTDa2 = tk.Toplevel()
    dTDa2.title('Error List')
    dTDaPT2 = pt.Table(dTDa2, dataframe=df1, showtoolbar=True, showstatusbar=True)
    dTDaPT2.show()
    Node.draw()
    # clear your list

    # label3 = tk.Label(root, text='Lexem ' + x1 + ' is:', font=('helvetica', 10))
    # canvas1.create_window(200, 210, window=label3)

    # label4 = tk.Label(root, text="Token_type"+x1, font=('helvetica', 10, 'bold'))
    # canvas1.create_window(200, 230, window=label4)


button1 = tk.Button(text='Scan', command=Scan, bg='brown', fg='white', font=('helvetica', 9, 'bold'))
canvas1.create_window(200, 180, window=button1)
root.mainloop()