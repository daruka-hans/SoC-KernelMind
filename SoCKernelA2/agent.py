import numpy as np

class ProbeAgent:
    hbins=np.linspace(0,1200,50)
    vbins=np.linspace(-100,10,50)

    qtable=np.zeros((51,51,3,2))

    alpha=0.1
    gamma=0.99
    epsilon=1.0
    epsilon_decay=0.999
    epsilon_min=0.01

    def discretize_state(self,raw_state):
        h,v,wind_idx=raw_state

        h_idx=np.digitize(h,self.hbins)
        v_idx=np.digitize(v,self.vbins)

        return (h_idx,v_idx,wind_idx)
    
    def choose_action(self,state):
        if np.random.random()<self.epsilon:
            return np.random.randint(0,2)
        else:
            h_idx,v_idx,wind_idx=state
            return np.argmax(self.qtable[h_idx,v_idx,wind_idx])
        
    def learn(self,state,action,reward,next_state,done):
        h,v,w=state
        nh,nv,nw=next_state

        present_q=self.qtable[h,v,w,action]

        if done:
            target_q=reward
        else:
            next_best=np.max(self.qtable[nh,nv,nw])
            target_q=reward+self.gamma*next_best

        self.qtable[h,v,w,action]+=self.alpha*(target_q-present_q)

        if self.epsilon>self.epsilon_min:
            self.epsilon*=self.epsilon_decay
        else:
            self.epsilon=0