function dm(amount) 
{
	string = "" + amount;
	dec = string.length - string.indexOf('.');
	if (string.indexOf('.') == -1)
	return string + '.00';
	if (dec == 1)
	return string + '00';
	if (dec == 2)
	return string + '0';
	if (dec > 3)
	return string.substring(0,string.length-dec+3);
	return string;
}

function enableTotal() {
	document.getElementById('total').disabled= "";
}


function calculate() {
	A = document.order.list1.value;
	B = document.order.list2.value;
	D = document.order.list4.value;
	E = document.order.list5.value;
	F = document.order.list6.value;
	G = document.order.list7.value;
	H = document.order.list8.value;
	I = document.order.list9.value;
	J = document.order.list10.value;
	K = document.order.list11.value;
	L = document.order.list12.value;
	M = document.order.list13.value;
	PrcA = 2.60;
	PrcB = 4.20;
	PrcD = 4.80;
	PrcE = 0.90;
	PrcF = 12.90;
	PrcG = 4.40;
	PrcH = 1.00;
	PrcI = 10.90;
	PrcJ = 9.00;
	PrcK = 1.30;
	PrcL = 1.80;
	PrcM = 45.00;
	TotA = A * PrcA;
	TotB = B * PrcB;
	TotD = D * PrcD;
	TotE = E * PrcE;
	TotF = F * PrcF;
	TotG = G * PrcG;
	TotH = H * PrcH;
	TotI = I * PrcI;
	TotJ = J * PrcJ;
	TotK = K * PrcK;
	TotL = L * PrcL;
	TotM = M * PrcM;
	X = TotA + TotB + TotD + TotE + TotF + TotG + TotH + TotI + TotJ + TotK + TotL + TotM;
	document.order.total.value = dm(X);
}
