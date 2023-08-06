from concurrent import futures
from multiprocessing import cpu_count

from estival.model import BayesianCompartmentalModel
from estival.utils import negative

# This is optional, just be silent if it's not installed...
try:
    import nevergrad as ng
except:
    pass

def get_instrumentation(priors, starting_points = None):
    idict = {}
    
    if starting_points is None:
        starting_points = {pk:p.ppf(0.5) for pk,p in priors.items()}
    
    for pk, p in priors.items():
        lower, upper = p.bounds()
        idict[pk] = ng.p.Scalar(starting_points[pk], lower=lower,upper=upper)
        
    return ng.p.Instrumentation(**idict)

class OptRunner:
    def __init__(self, optimizer, min_func, num_workers):
        self.optimizer = optimizer
        self.min_func = min_func
        self.num_workers = num_workers
        
    def minimize(self, budget):
        cur_ask = self.optimizer.num_ask
        self.optimizer.budget = cur_ask + budget
        with futures.ThreadPoolExecutor(max_workers=self.num_workers) as executor:
            rec = self.optimizer.minimize(self.min_func, executor=executor)
        return rec
    
def optimize_model(bcm: BayesianCompartmentalModel, budget: int = 1000, opt_class=ng.optimizers.NGOpt, num_workers: int = None):
    if not num_workers:
        num_workers = cpu_count()

    instrum = get_instrumentation(bcm.priors)
    min_func = negative(bcm.loglikelihood)
    optimizer = opt_class(parametrization=instrum, budget=budget, num_workers=num_workers)
    return OptRunner(optimizer, min_func, num_workers)