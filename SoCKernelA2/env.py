import numpy as np

class ProbeEnv:
    m=1000.0
    g=13.7
    R_ad=10700000.0
    k_dr=2.0
    F_th=25000.0
    dt=0.1
    max_steps=2000
    drop_height=1000.0

    wind_mult=[1.0,1.5,2.0]

    wind_TPM=np.array([
        [0.7,0.2,0.1],
        [0.2,0.6,0.2],
        [0.2,0.3,0.5]
    ])

    def reset(self):
        self.h=self.drop_height
        self.v=0.0
        self.steps=0
        self.wind_idx=0
        return (self.h,self.v,self.wind_idx)

    def step(self,action):
        self.steps+=1

        probs=self.wind_TPM[self.wind_idx]
        self.wind_idx=np.random.choice([0,1,2],p=probs)
        wind_multiplier=self.wind_mult[self.wind_idx]

        f_gr=-self.m*self.g*(1-self.h/self.R_ad)
        f_th=self.F_th if action == 1 else 0.0
        f_dr=self.k_dr*self.v**2*np.sign(-self.v)*wind_multiplier

        f_net=f_gr+f_th+f_dr

        a=f_net/self.m
        self.v+=a*self.dt
        self.h+=self.v*self.dt

        reward=0.0
        done=False

        if action==1:
            reward-=0.5 #fuel cost
        
        reward-=(self.h/1000)*0.5  #small reward for descending

        if self.h<=0 and self.v>=-3.0:  #soft landing
            reward+=500
            done=True

        if self.h<=0 and self.v<-3.0:
            reward+=-200+(self.v*2)
            done=True

        if self.h>1200 or self.steps>self.max_steps:
            reward-=200
            done=True
        
        return ((self.h,self.v,self.wind_idx),reward,done)


