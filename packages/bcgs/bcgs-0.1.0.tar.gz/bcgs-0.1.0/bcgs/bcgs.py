import numpy as np
import scipy.stats as st

class NotConjugateError(Exception):
    def __init__(self):
        Exception.__init__(self, "Non-conjugate (or not implemented) conditional dependence detected")


class Parameter:
    def __init__(self, value=None, data=None):
        self.value = value
        self.data = data # NB we will be lazy and use (data is not None) to mean "fixed"
        if self.data is not None:
            self.value = self.data
        if self.value is None:
            raise Exception("Parameters must be given a starting value if they are not data")
        self.value = np.array(self.value)
        self.size = np.size(self.value)
        self.targets = []
        self.determines = []
    def update(self):
        if self.data is None:
            self._update()
            for p in self.determines:
                p.update()
        return self.value

class Deterministic(Parameter):
    def __init__(self, function, *args, **kwargs): # args and kwargs are Parameters whose values are to be passed to the function
        value = function(*[p.value for p in args], **{k:kwargs[k].value for k in kwargs.keys()})
        Parameter.__init__(self, data=value) # setting data to "not None" so we are seen as fixed
        self.function = function
        self.args = args
        self.kwargs = kwargs
        for p in args:
            p.determines.append(self)
        for k in kwargs.keys():
            kwargs[k].determines.append(self)
    def update(self): # NB overrides Parameter.update
        self.value = self.function(*[p.value for p in self.args], **{k:self.kwargs[k].value for k in self.kwargs.keys()})
        return self.value

class Constant(Parameter):
    def __init__(self, *args, **kwargs):
        Parameter.__init__(self, *args, **kwargs)
        self.data = self.value # setting data to "not None" so we are seen as fixed
    def _update(self):
        pass

class Poisson(Parameter):
    def __init__(self, mean, *args, **kwargs):
        Parameter.__init__(self, *args, **kwargs)
        if not isinstance(mean, (Constant, Deterministic, Gamma)):
            raise NotConjugateError
        self.mean = mean
        mean.targets.append(self)
    def _update(self):
        self.value = st.poisson.rvs(self.mean.value, size=self.size)

class Gamma(Parameter):
    def __init__(self, shape, rate, *args, **kwargs):
        Parameter.__init__(self, *args, **kwargs)
        if not isinstance(shape, (Constant, Deterministic)): # shape is conjugate to Gamma again (not implemented)
            raise NotConjugateError
        self.shape = shape
        shape.targets.append(self)
        if not isinstance(rate, (Constant, Deterministic)): # rate is conjugate to something (not implemented)
            raise NotConjugateError
        self.rate = rate
        rate.targets.append(self)
    def _update(self):
        N = np.sum([np.sum(t.value) for t in self.targets])
        m = np.sum([np.size(t.value) for t in self.targets])
        self.value = st.gamma.rvs(self.shape.value+N, scale=1./(self.rate.value+m), size=self.size)

class Binomial(Parameter):
    def __init__(self, p, n, *args, **kwargs):
        Parameter.__init__(self, *args, **kwargs)
        if not isinstance(p, (Constant, Deterministic, Beta)):
            raise NotConjugateError
        self.p = p
        p.targets.append(self)
        if not isinstance(n, (Constant)):
            raise Exception("Number of trials for the Binomial distribution must be Constant")
        self.n = n
        n.targets.append(self)
    def _update(self):
        self.value = st.binom.rvs(self.n.value, self.p.value, size=self.size)

class Bernoulli(Binomial):
    def __init__(self, p, *args, **kwargs):
        n = Constant(value=1)
        Binomial.__init__(self, p, n, *args, **kwargs)

class Beta(Parameter):
    def __init__(self, alpha, beta, *args, **kwargs):
        Parameter.__init__(self, *args, **kwargs)
        if not isinstance(alpha, (Constant, Deterministic)): # possible todo
            raise NotConjugateError
        self.alpha = alpha
        alpha.targets.append(self)
        if not isinstance(beta, (Constant, Deterministic)): # possible todo
            raise NotConjugateError
        self.beta = beta
        beta.targets.append(self)
    def _update(self):
        k = np.sum([np.sum(t.value) for t in self.targets])
        n = np.sum([np.sum(t.n.value) for t in self.targets])
        self.value = st.beta.rvs(self.alpha.value+k, self.beta.value+n-k, size=self.size)

class Normal(Parameter):
    def __init__(self, mean, variance, *args, **kwargs):
        Parameter.__init__(self, *args, **kwargs)
        if not isinstance(mean, (Constant, Deterministic, Normal)):
            raise NotConjugateError
        self.mean = mean
        mean.targets.append(self)
        if not isinstance(variance, (Constant, Deterministic, ScaledInverseChisquare)):
            raise NotConjugateError
        self.variance = variance
        variance.targets.append(self)
    def _update(self):
        tmpv = 1.0 / self.variance.value
        tmpm = self.mean.value / self.variance.value
        for t in self.targets:
            tmpv += np.size(t.value) / t.variance.value
            tmpm += np.sum(t.value) / t.variance.value
        tmpv = 1.0 / tmpv
        self.value = st.norm.rvs(tmpv*tmpm, np.sqrt(tmpv), size=self.size)

class ScaledInverseChisquare(Parameter):
    def __init__(self, dof, variance, *args, **kwargs):
        Parameter.__init__(self, *args, **kwargs)
        if not isinstance(dof, (Constant, Deterministic)): # possible todo
            raise NotConjugateError
        self.dof = dof
        dof.targets.append(self)
        if not isinstance(variance, (Constant, Deterministic)): # possible todo
            raise NotConjugateError
        self.variance = variance
        variance.targets.append(self)
    def _update(self):
        df = self.dof.value.copy() # copy to avoid changing self.dof.value below
        s2 = self.dof.value * self.variance.value
        for t in self.targets:
            df += np.size(t.value)
            s2 += np.sum((t.value - t.mean.value)**2)
        self.value = s2 / st.chi2.rvs(df=df, size=self.size)



class Model:
    def __init__(self):
        self.everything = {}
        self.free = []
        self.trace = []
    def __getattr__(self, name):
        return self.everything[name]
    def add(self, name, expression, trace=None):
        if name in self.everything.keys():
            raise Exception("moo")
        self.everything[name] = expression
        if expression.data is None:
            self.free.append(name)
        if trace is None:
            trace = (expression.data is None or isinstance(expression, Deterministic)) # False for data and Constants
        if trace:
            self.trace.append(name)
    def update(self):
        # could have generated a random order for updating everything in self.free by default, or let the user specify
        for name in self.free:
            self.everything[name].update()
    def run_chain(self, steps=0):
        chain = {name:np.full((steps,np.size(self.everything[name].value)), np.nan) for name in self.trace}
        for i in range(steps):
            self.update()
            for name in self.trace:
                chain[name][i] = self.everything[name].value.flatten()
        return chain
    def chain_dict_to_array(self, chain):
        names = []
        for name in self.trace:
            if self.everything[name].size == 1:
                names.append(name)
            else:
                names += [name+'_'+str(i) for i in range(self.everything[name].size)]
        return (names, np.hstack([chain[name] for name in self.trace]))
