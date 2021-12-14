
function [D, R] = LinearAntenna( L, theta )
    eta = 120*pi;
    F = 20e9; % 20GHz
    wl = (1/F)*physconst('LightSpeed');
    k = (2*pi)/wl;
    
    f1 = @(x) cos(x)./x;
    C = @(x) integral( f1, -Inf, x );
    f2 = @(x) sin(x)./x;
    S = @(x) integral( f2, -Inf, x );
    
    R = (eta/2*pi)*( 0.5772 + log(k*L) - C(k*L) + 0.5*(S(2*k*L) - 2*S(k*L))*sin(k*L) + 0.5*(0.5772 + log(k*L/2) + C(2*k*L) - 2*C(k*L))*cos(k*L) );
    Q = 0.5772 + log(k*L) - C(k*L) + 0.5*(S(2*k*L) - 2*S(k*L))*sin(k*L) + 0.5*(0.5772 + log(k*L/2) + C(2*k*L) - C(k*L))*cos(k*L);
    D = (2/Q)*( ( cos((k*L/2)*cos(theta)) - cos(k*L/2) )/sin(theta) )^2;
end