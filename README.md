# landing_scheduling

The plane movements in large airports are subject to numerous security constraints. The problem presented in this section consist of calculating a schedule for flight landings on a single runway. More general problems have been studied but they are fairly complicated (dynamic cases, for instance through planes arriving late, instances with several runways, etc.).
Ten planes are due to arrive. Every plane has an earliest arrival  time (time when the plane arrives above the zone if traveling at maximum speed) and a latest arrival time (influenced among other things by its fuel supplies). Within this time window the airlines choose a target time, communicated to the public as the flight arrival time. The early or late arrival of an aircraft with respect to its target time leads to disruption of the airport and causes costs. To take into account these cost and to compare them more
easily, a penalty per minute of early arrival and a second penalty per minute of late arrival are associated with every plane. The time windows (in minutes from the start of the day) and the   penalties per plane are given in the following table.

>Flight             | 1  | 2  | 3  | 4  | 5  | 6  | 7  | 8  | 9  | 10 |
>---                | ---| ---| ---| ---| ---| ---| ---| ---| ---| ---|
>Earliest arrival   | 129| 195|  89|  96| 110| 120| 124| 126| 135| 160|
>Target time        | 155| 258|  98| 106| 123| 135| 138| 140| 150| 180|
>Latest arrival     | 559| 744| 510| 521| 555| 576| 577| 573| 591| 657|
> Earliness penalty |  10|  10|  30|  30|  30|  30|  30|  30|  30|  30|
> Lateness penalty  |  10|  10|  30|  30|  30|  30|  30|  30|  30|  30|

Due to turbulence and the duration of the time during which a plane is on the runway, a security interval has to separate any two landings. An entry in line p of column q in the following Table 11.5 denotes the minimum time interval (in minutes) that has to lie between the landings of planes p and q, even if they are not consecutive. Which landing schedule minimizes the total penalty subject to arrivals within the given time windows and the required intervals separating any two landings?

>|   | 1  | 2  | 3  | 4  | 5  | 6  | 7  | 8  | 9  | 10 |
> ---| ---| ---| ---| ---| ---| ---| ---| ---| ---| ---|
> 1  |   -|   3|  15|  15|  15|  15|  15|  15|  15|  15|
> 2  |   3|   -|  15|  15|  15|  15|  15|  15|  15|  15|
> 3  |  15|  15|   -|   8|   8|   8|   8|   8|   8|   8|
> 4  |  15|  15|   8|   -|   8|   8|   8|   8|   8|   8|
> 5  |  15|  15|   8|   8|   -|   8|   8|   8|   8|   8|
> 6  |  15|  15|   8|   8|   8|   -|   8|   8|   8|   8|
> 7  |  15|  15|   8|   8|   8|   8|   -|   8|   8|   8|
> 8  |  15|  15|   8|   8|   8|   8|   8|   -|   8|   8|
> 9  |  15|  15|   8|   8|   8|   8|   8|   8|   -|   8|
> 10 |  15|  15|   8|   8|   8|   8|   8|   8|   8|   -|

## MILP formulation
## Sets
$\mathcal{F}$: all flights to schedule

### Parameters
$T_f$: target landing time for flight $f \in \mathcal{F}$ \\
$E_f$: earliest landing time for flight $f \in \mathcal{F}$ \\
$L_f$: latest landing time for flight $f \in \mathcal{F}$ \\
$P^E_f$: earliness penalty  for flight $f \in \mathcal{F}$ \\
$P^T_f$: tardiness penalty  for flight $f \in \mathcal{F}$ \\
$MIN_{ff'}$: minimum separation between 

### Variables
$l_f$: landing time for flight $f \in \mathcal{F}$ \\
$e_f$: earliness of flight $f \in \mathcal{F}$ \\
$t_f$: tardiness of flight $f \in \mathcal{F}$ \\
$\alpha_{ff'}$: 1 if flight $f \in \mathcal{F}$ preceeds flight $f' \in \mathcal{F}$, 0 otherwise

### MILP model
minimize $\sum_t P^E_fe_f + \sum_t P^T_ft_f$ \\
subject to: \\
$\alpha_{ff'} + \alpha_{f'f} = 1 \;\;\; \forall f, f' \in \mathcal{F}, f \neq f'  $ \\
$t_f \leq E_f \;\;\; \forall f \in \mathcal{F}$ \\
$t_f \geq L_f \;\;\; \forall f \in \mathcal{F}$ \\
$t_f' \geq t_f + MIN_{ff'} - M  \left(1- \alpha_{ff'}\right) \;\;\; \forall f, f' \in \mathcal{F}, f \neq f'$ \\
$e_f \geq T_f - t_f \;\;\; \forall f \in \mathcal{F}$ \\
$t_f \geq t_f - T_f \;\;\; \forall f \in \mathcal{F}$ \\
