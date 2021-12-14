
function [f1, f2] = Test1_DebEtAl( varargin )
    X = zeros(1,length(varargin));
    for i=1:length(varargin)
        X(i) = varargin{i};
    end
    
    f1 = X(1);
    g = 1 + 9*sum(X(2:length(X)))/29;
    h = 1 - sqrt(f1/g);
    f2 = g*h;
end