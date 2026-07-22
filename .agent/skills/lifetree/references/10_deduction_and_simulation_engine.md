# 10. Multi-Step Temporal Deduction & Simulation Engine Architecture

## 1. Executive Summary & Mathematical Framework
The Multi-Step Temporal Deduction Engine provides multi-year trajectory forecasting across competing decision branches ($B_A, B_B, \dots, B_N$) over a temporal horizon of $T \in [1, 10]$ years.

Unlike static rule evaluation, the deduction engine models dynamic state mutation over time $t$:

$$S(t+1) = f(S(t), A(t), E(t), \theta)$$

Where:
- $S(t)$: User State Vector at year $t$ (Capital balance $K(t)$, Language level $L(t)$, Work experience $W(t)$, Visa status $V(t)$).
- $A(t)$: User Personal Action executed at year $t$.
- $E(t)$: External Macro Shock event vector (Statutory deposit hike $\Delta K$, embassy processing delay $\Delta t$).
- $\theta$: Domain Rule Pack parameter matrix.

---

## 2. Multi-Branch Trajectory Calculation

### 2.1 State Vector Definition
$$S_i(t) = \begin{bmatrix}
K_i(t) & \text{Capital Reserve (USD)} \\
L_i(t) & \text{Language Level (Ordinal A1..C2)} \\
W_i(t) & \text{Cumulative Work Experience (Years)} \\
P_i(t) & \text{Cumulative Success Probability (\%)}
\end{bmatrix}$$

### 2.2 Plan B Trigger Threshold Condition
A Plan B side bud branch is dynamically sprouted when the success probability drops below the safety threshold $\tau_{\text{safe}} = 0.60$:

$$\text{Sprout\_Plan\_B}(t) = \begin{cases} \text{TRUE} & \text{if } P_i(t) < 0.60 \\ \text{FALSE} & \text{otherwise} \end{cases}$$

---

## 3. Dynamic Shock Injection Algorithm

```python
def inject_macro_shock(state_vector, shock_event):
    """
    Applies real-time macro shock mutations to state vector.
    """
    if shock_event["type"] == "STATUTORY_CAPITAL_HIKE":
        state_vector["capital_balance_usd"] -= shock_event["amount_usd"]
        state_vector["success_prob"] *= 0.90
    elif shock_event["type"] == "EMBASSY_PROCESSING_DELAY":
        state_vector["timeline_months"] += shock_event["delay_months"]
        state_vector["success_prob"] *= 0.85
    return state_vector
```

---

## 4. Interactive HTML Deduction Scenario Player Integration
The deduction engine outputs JSON trajectories to [deduction_player_html.py](file:///Users/cary/Desktop/Fun/LifeTree/.agent/skills/lifetree/scripts/ui_translators/deduction_player_html.py), rendering the standalone interactive player [lifetree_deduction_player.html](file:///Users/cary/Desktop/Fun/LifeTree/.agent/skills/lifetree/examples/lifetree_deduction_player.html).
