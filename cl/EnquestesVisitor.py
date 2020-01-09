# Generated from Enquestes.g by ANTLR 4.7.2
from antlr4 import *
import networkx as nx
if __name__ is not None and "." in __name__:
    from .EnquestesParser import EnquestesParser
else:
    from EnquestesParser import EnquestesParser


class EnquestesVisitor(ParseTreeVisitor):

    G = nx.DiGraph()
    items = {}

    # Visit a parse tree produced by EnquestesParser#root.
    def visitRoot(self, ctx: EnquestesParser.RootContext):
        self.G = nx.DiGraph()
        self.items = {}
        return self.visitChildren(ctx)

    def getGraph(self):
        return self.G

    # Visit a parse tree produced by EnquestesParser#inst.
    def visitInst(self, ctx: EnquestesParser.InstContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by EnquestesParser#pregunta.
    def visitPregunta(self, ctx: EnquestesParser.PreguntaContext):
        g = ctx.getChildren()
        L = [next(g) for i in range(5)]
        id = L[0].getText()
        frase = self.visit(L[3]) + "?"
        self.G.add_node(id, pregunta=frase, type='pregunta')

    # Visit a parse tree produced by EnquestesParser#resposta.
    def visitResposta(self, ctx: EnquestesParser.RespostaContext):
        num = ctx.getChildCount()
        g = ctx.getChildren()
        L = [next(g) for i in range(num)]
        id = L[0].getText()
        opcions = {}
        for j in range(3, num):
            optnum, opttext = self.visit(L[j])
            opcions[optnum] = opttext
        self.G.add_node(id, res=opcions, type='resposta')

    # Visit a parse tree produced by EnquestesParser#item.
    def visitItem(self, ctx: EnquestesParser.ItemContext):
        g = ctx.getChildren()
        L = [next(g) for i in range(6)]
        idI = L[0].getText()
        idP = L[3].getText()
        idR = L[5].getText()
        self.G.add_edge(idP, idR, id=idI, type='item')
        self.items[idI] = idP

    # Visit a parse tree produced by EnquestesParser#alternativa.
    def visitAlternativa(self, ctx: EnquestesParser.AlternativaContext):
        num = ctx.getChildCount()
        g = ctx.getChildren()
        L = [next(g) for i in range(num)]
        aid = L[0].getText()
        iid = L[3].getText()
        pid = self.items[iid]
        for j in range(5, num - 1, 2):
            rnum, item = self.visit(L[j])
            p2id = self.items[item]
            self.G.add_edge(pid, p2id, resposta=rnum, type='alternativa')

    # Visit a parse tree produced by EnquestesParser#opcio.
    def visitOpcio(self, ctx: EnquestesParser.OpcioContext):
        g = ctx.getChildren()
        L = [next(g) for i in range(4)]
        index = int(L[0].getText())
        txt = self.visit(L[2])
        return index, txt

    # Visit a parse tree produced by EnquestesParser#assig.
    def visitAssig(self, ctx: EnquestesParser.AssigContext):
        g = ctx.getChildren()
        L = [next(g) for i in range(4)]
        rnum = L[1].getText()
        item = L[3].getText()
        return rnum, item

    # Visit a parse tree produced by EnquestesParser#enquesta.
    def visitEnquesta(self, ctx: EnquestesParser.EnquestaContext):
        num = ctx.getChildCount()
        g = ctx.getChildren()
        L = [next(g)for i in range(num)]
        title = L[0].getText()
        end = L[num - 1].getText()
        self.G.add_node(title, type='enquesta_init')
        self.G.add_node(end, type='enquesta_end')
        anterior = title
        for j in range(3, num - 1):
            id = self.items[L[j].getText()]
            self.G.add_edge(anterior, id, type='enquesta')
            anterior = id
        self.G.add_edge(anterior, end, type='enquesta')
        self.G.graph['title'] = title

    # Visit a parse tree produced by EnquestesParser#frase.
    def visitFrase(self, ctx: EnquestesParser.FraseContext):
        num = ctx.getChildCount()
        g = ctx.getChildren()
        L = [next(g).getText() for i in range(num)]
        s = " ".join(L)
        return s
