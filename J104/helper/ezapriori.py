from dataclasses import dataclass
from pyvis.network import Network
from apyori import apriori

def frozenset(x):
    return ''.join(x)

@dataclass
class EZApriori:
    TRANSACTION: list
    LEN: int = 2
    
    def fit(self, SUPPORT, CONFIDENCE):
        
        AprioriRule = apriori(
            transactions=self.TRANSACTION, 
            min_support=SUPPORT, 
            min_confidence=CONFIDENCE, 
            min_length=self.LEN, 
            max_length=self.LEN
        )
        list_From, list_To, list_Weight = self._ExtractRule(AprioriRule)
        fname = f'S_{SUPPORT:.3f}_C_{CONFIDENCE:.3f}'
        self._PlotNetwork(list_From, list_To, list_Weight, fname)
    
    def _ExtractRule(self, APRIORI_RULE):
        list_From = []
        list_To = []
        list_Weight = []

        for product in APRIORI_RULE:
            try:
                FROM = eval(str(product[2][0][1]))
                TO = eval(str(product[2][0][0]))

                list_From.append(FROM)
                list_To.append(TO)
                list_Weight.append(1)

            except:
                pass
        
        return list_From, list_To, list_Weight
    
    def _PlotNetwork(self, FROM, TO, WEIGHT, FNAME):

        canvas = Network(height='100%', width='100%', bgcolor='#fff', font_color='#3B3838')

        for e in zip(FROM, TO, WEIGHT):
            _from = e[0]
            _to = e[1]
            _w = e[2]

            canvas.add_node(_from, _from, title=_from, color='#C0AA7A', borderWidth=0, size=40)
            canvas.add_node(_to, _to, title=_to, color='#F2F2F2', borderWidth=0, size=20)
            canvas.add_edge(_from, _to, value=_w)

        neighbor_map = canvas.get_adj_list()

        
        for node in canvas.nodes:
            node['title'] += ' → ' + ' '.join(neighbor_map[node['id']])
            
        canvas.write_html(f'Images/Plot_Apriori__{FNAME}.html')