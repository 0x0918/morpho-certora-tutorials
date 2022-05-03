methods {
    balanceOf(address) returns (uint256) envfree;
    totalSupply()      returns (uint256) envfree;
}

// totalSupply is sum of balanceOf(user) for all users
ghost mathint sum_of_balances {
    init_state axiom sum_of_balances == 0;
}

hook Sstore balances[KEY address user] uint256 newValue (uint256 oldValue) STORAGE {
    sum_of_balances = sum_of_balances + newValue - oldValue;
}

invariant totalSupplyIsSumOfBalances()
    totalSupply() == sum_of_balances

rule transferPreserveSupply {
    address sender; address receiver;
    uint amount; env e;
    require sender == e.msg.sender;
    mathint supplyBefore = totalSupply();
    address u1; address u2;
    require forall address a1. forall address a2. balanceOf(a1) + balanceOf(a2) <= totalSupply();


    transfer(e, receiver, amount);

    mathint supplyAfter = totalSupply();
    mathint balanceAfterUser1 = balanceOf(u1);
    mathint balanceAfterUser2 = balanceOf(u2);

    assert(supplyBefore == supplyAfter);
    assert(balanceAfterUser1 + balanceAfterUser2 <= supplyAfter);
}

invariant userBalanceBounded(address userA, address userB)
    balanceOf(userA) + balanceOf(userB) <= totalSupply()
