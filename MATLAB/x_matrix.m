function [TM, TMP] = x_matrix(thetai, thetat, N1, N2)
%   thetat=asin(Na/N1*sin(thetai));
%   Fresnel equation
    taf = 2*N1*cos(thetai)/(N1*cos(thetai)+N2*cos(thetat));
    raf = (N1*cos(thetai)-N2*cos(thetat))/(N1*cos(thetai)+N2*cos(thetat));

    tpaf = 2*N1*cos(thetai)/(N1*cos(thetat)+N2*cos(thetai));
    rpaf = (N1*cos(thetat) - N2*cos(thetai))/(N1*cos(thetat)+N2*cos(thetai));
    
    TM = [1/taf  raf/taf;  raf/taf  1/taf];
    TMP = [1/tpaf  rpaf/tpaf;  rpaf/tpaf  1/tpaf];
end
