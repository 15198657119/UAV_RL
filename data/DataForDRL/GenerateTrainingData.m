data = {};

IT = 100;

tic;
for i=1:IT

	addpath('env')
	addpath('utils');
	addpath('trials');
	addpath('api');
	addpath('sp');


	devNum = 4;
	slotNum = 20;
	range = [0.2,0.5];
	slotInternal = 0.5;
	devPostion = randi([0,100],2,devNum);
	% devPostion = [55,60,42,44,97,79,57,7,2,78;72,55,65,90,38,53,93,8,84,87];

	InitParameters(devPostion,slotNum,slotInternal)
	total = InitTaskMatrix(range);


	iteration = 10;
	accuracy = 10^-4;


	global Q0 QF D Tk K N M S W C Ck E
	QF = [M;0];
	Tasks = S;
	Ck = 2;
	% 	C = 0;
	C = randi([0,30]);

	try
		[ok,res] = StartTrial(iteration,accuracy);
		if ok
			data{i} = [K, N, D, Tk, C, Ck, E, Q0', QF', reshape(devPostion,1,2*K), reshape(Tasks,1,K*N), reshape(res.q,[1,2*N]), ...
				reshape(res.a,1,K*N),reshape(res.b,1,K*N),reshape(res.f,1,K*N),reshape(res.l,1,K*N)];
		end
	catch ME
		ME.message
		continue;
	end
end

t=toc
disp(t)
disp(toc - tic);

[~,i] = size(data);
data = reshape(data,i,1);

csvwrite('./data/DataForDRL/K4/data_7.csv',data);