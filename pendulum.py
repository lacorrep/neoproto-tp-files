import numpy as np
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.integrate import odeint
from scipy.constants import g
from dataclasses import dataclass
from typing import  Any, Dict, Union, Optional, Self

# RESULTS_DIR = "results"
figures_DPI = 100

@dataclass
class DoublePendulum:
    l1: float
    l2: float
    m1: float
    m2: float
    def __post_init__(self):
        self.l1 = float(self.l1)
        self.l2 = float(self.l2)
        self.m1 = float(self.m1)
        self.m2 = float(self.m2)

class Simulator:
    def __init__(self, p: DoublePendulum,  params: Dict[str, Any]):
        self.p: DoublePendulum = p
        self.theta_init = np.array(params["theta_init"])
        self.time_s = params["time_s"]
        self.time_step_s = params["time_step_s"]
        if "integration_method" not in params:
            params["integration_method"] = None
        self.integration_method = params["integration_method"] or "auto"
        self.u: Union[np.ndarray, None] = None
        self.time_vec: Union[np.ndarray, None] = None
        self.x: Union[np.ndarray, None] = None
        self.z: Union[np.ndarray, None] = None


    def mvt_eq(self, u: np.array, t: float) -> np.array:
        delta = u[2] - u[0]
        denom_1 = (self.p.m1+self.p.m2)*self.p.l1 - self.p.m2*self.p.l1*np.cos(delta)**2
        denom_2 = (self.p.l2/self.p.l1)*denom_1
        dudt = np.array([
            u[1],
            (self.p.m2*self.p.l1*(u[1]**2)*np.sin(delta)*np.cos(delta) \
            + self.p.m2*g*np.sin(u[2])*np.cos(delta) \
            + self.p.m2*self.p.l2*(u[3]**2)*np.sin(delta) \
            - (self.p.m1+self.p.m2)*g*np.sin(u[0])) \
            / denom_1,
            u[3],
            (-self.p.m2*self.p.l2*(u[3]**2)*np.sin(delta)*np.cos(delta) \
             + (self.p.m1+self.p.m2)*g*np.sin(u[0])*np.cos(delta) \
             - (self.p.m1+self.p.m2)*self.p.l1*(u[1]**2)*np.sin(delta) \
             - (self.p.m1+self.p.m2)*g*np.sin(u[2])) \
            / denom_2])
        return dudt

    def run(self) -> Self:
        print("Starting run...")
        time_vec = np.arange(0.0, self.time_s+self.time_step_s, self.time_step_s)
        run_t_start = time.time()
        if self.integration_method == "auto":
            u = odeint(self.mvt_eq, self.theta_init, time_vec)
        elif self.integration_method == "euler":
            u = [self.theta_init]
            for t in time_vec[:-1]:
                u.append( u[-1] + self.time_step_s*self.mvt_eq(u[-1], t) )
            u = np.array(u)
        run_t_end = time.time()
        run_duration = run_t_end - run_t_start
        print(f"Run executed successfully ({run_duration:.2f})")
        result = np.column_stack((time_vec, u))
        self.time_vec = result[:, 0]
        self.u = result[:, 1:]
        self.x = np.array([self.p.l1*np.sin(self.u[:, 0]),
                      self.p.l2*np.sin(self.u[:, 2]) + self.p.l1*np.sin(self.u[:, 0])
                     ])
        self.z = np.array([-self.p.l1*np.cos(self.u[:, 0]),
                      -self.p.l2*np.cos(self.u[:, 2]) - self.p.l1*np.cos(self.u[:, 0])
                     ])
        return self


    def plot_angles(self, save_to_file: Optional[str] = None) -> None:
        fig, ax = plt.subplots(figsize=(12, 6), dpi=figures_DPI)
        ax.plot(self.time_vec, np.sin(self.u[:, 0]), label=r"$ \theta_1 $", color="blue")
        ax.plot(self.time_vec, np.sin(self.u[:, 2]), label=r"$ \theta_2 $", color="red")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel(r"$\sin(\theta)$")
        ax.set_title(r"Evolution temporelle de $\sin(\theta)$")
        ax.grid(linestyle="dotted")
        ax.legend()
        if save_to_file:
            fig.savefig(save_to_file)


    def plot_portrait_phase(self, save_to_file: Optional[str] = None) -> None:
        fig, ax = plt.subplots(1, 2, figsize=(12, 6), dpi=figures_DPI)
        ax[0].plot(self.u[:, 0], self.u[:, 1], color="blue")
        ax[0].set_xlabel(r"$\theta_1$")
        ax[0].set_ylabel(r"$\dot{\theta_1}$")
        ax[0].set_title("Espace des phases M1")
        ax[0].grid(linestyle="dotted")
        ax[1].plot(self.u[:, 2], self.u[:, 3], color="red")
        ax[1].set_xlabel(r"$\theta_2$")
        ax[1].set_ylabel(r"$\dot{\theta_2}$")
        ax[1].set_title("Espace des phases M2")
        ax[1].grid(linestyle="dotted")
        plt.show()
        if save_to_file:
            fig.savefig(save_to_file)


    def plot_trajectory(self, save_to_file: Optional[str] = None) -> None:
        fig, ax = plt.subplots(figsize=(12, 6), dpi=figures_DPI)
        ax.plot(self.x[0, :], self.z[0, :], label="M1", color="blue")
        ax.plot(self.x[1, :], self.z[1, :], label="M2", color="red")
        ax.set_xlabel("x(m)")
        ax.set_ylabel("z(m)")
        ax.set_title("Trajectoire des pendules M1 et M2")
        ax.grid(linestyle="dotted")
        ax.legend()
        plt.show()
        if save_to_file:
            fig.savefig(save_to_file)


    def animate_trajectory(self, save_to_file: Optional[str] = None) -> animation.FuncAnimation:
        max_l = self.p.l1 + self.p.l2
        fig = plt.figure(figsize=(6, 6), dpi=figures_DPI)
        ax = fig.add_subplot(autoscale_on=False, xlim=(-max_l, max_l), ylim=(-max_l, 1.))
        ax.set_aspect('equal')
        ax.grid()
        line, = ax.plot([], [], 'o-', lw=2)
        trace, = ax.plot([], [], '.-', lw=1, ms=2)
        time_template = 'time = %.1fs'
        time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)
        def animate(i):
            thisx = [0, self.x[0, :][i], self.x[1, :][i]]
            thisy = [0, self.z[0, :][i], self.z[1, :][i]]
            history_x = self.x[1, :][:i]
            history_y = self.z[1, :][:i]
            line.set_data(thisx, thisy)
            trace.set_data(history_x, history_y)
            time_text.set_text(time_template % (i*self.time_step_s))
            return line, trace, time_text
        ani = animation.FuncAnimation(fig,
                                      animate,
                                      len(self.z[0, :]),
                                      interval=self.time_step_s*1000,
                                      blit=True)
        return ani
