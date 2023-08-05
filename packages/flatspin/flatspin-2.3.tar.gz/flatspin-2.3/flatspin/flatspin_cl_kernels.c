#pragma OPENCL EXTENSION cl_khr_fp64 : enable

int d2_to_d1(int x, int y, int nx) {
    return x * nx + y;
}

double2 external_field(int i, __global char * spin, __global double2 * m, __global double2 * h_ext)
{
    //printf("H_EXT: %f %f\n", h_ext.x, h_ext.y);
    //printf("M: %f %f\n", m[i].x, m[i].y);

    //m = self.spin[i] * self.m[i]
    //m_angle = np.arctan2(m[1], m[0])
    double m_angle = atan2(spin[i] * m[i].y, spin[i] * m[i].x);


    //h_ext = self.h_ext[i]
    double h = length(h_ext[i]);
    //h = norm(h_ext)
    double h_angle = atan2(h_ext[i].y, h_ext[i].x);
    //h_angle = np.arctan2(h_ext[1], h_ext[0])

    double theta = h_angle - m_angle;

    double2 h_par_perp;
    h_par_perp.x = h*cos(theta);
    h_par_perp.y = h*sin(theta);

    //double h_par = h*cos(theta);
    //double h_perp = h*sin(theta);

    return h_par_perp;
}

double2 h_dip_local(
        int i,
        __global char * spin,
        __global double2 * h_dip_cache,
        double alpha,
        __global int * neighbors,
        int n_neighbors) {



    double2 h_dip = {0, 0};

    //all neighbors

    //h_dip_cache is a 2d array index on (spin, neighbor) = <num>
    //same with neighbors-array
    //iterate neighbors
    for(int n = 0; n < n_neighbors; n++) {
        int cached_i = d2_to_d1(i, n, n_neighbors);
        int neighbor_ii = cached_i;

        int neighbor_i = neighbors[neighbor_ii];
        if(neighbor_i == -1) {
            break;
        }

        //printf("(%d, %d) neighbor num %d index %d, spin on site %d spin on neighbor: %d\\n", x, y, n, neighbor_i, spin[i], spin[neighbor_i]);

        h_dip += h_dip_cache[cached_i] * spin[i] * spin[neighbor_i];
    }


    return alpha * h_dip;
  }



__kernel void total_fields(
        __global char * spin,
        __global double2 * h_dip_cache,
        __global double * alpha,
        __global double2 * res,
        __global int * neighbors,
        __global int * n_neighbors,
        __global double2 * m,
        __global double2 * h_ext)
{
    int i = get_global_id(0);


    res[i] = h_dip_local(i, spin, h_dip_cache, *alpha, neighbors, *n_neighbors) +\
            external_field(i, spin, m, h_ext);
}

__kernel void test_h_dip_local(
        __global char * spin,
        __global double2 * h_dip_cache,
        __global double * alpha,
        __global double2 * res,
        __global int * neighbors,
        __global int * n_neighbors
        )
{
    int i = get_global_id(0);
    res[i] = h_dip_local(i, spin, h_dip_cache, *alpha, neighbors, *n_neighbors);
}

__kernel void test_h_ext(
        __global char * spin,
        __global double2 * m,   //1d array of 2-tuples
        __global double2 * h_ext,
        __global double2 * res
        )
{
    int i = get_global_id(0);
    res[i] = external_field(i, spin, m, h_ext);
}



//Calculate the dipolar interaction from this spin(i,j)
//with all of it's neighbors.
__kernel void spin_dipolar_field(  __global double2 * pos,
                                        __global double2 * h_dip,
                                        __global int * neighbors,
                                        __global int * n_neighbors,
                                        __global double2 * m
                                      )
{


    int i = get_global_id(0);   //spin index
    int q = get_global_id(1);   //neighbor index

    //one thread for each neighbor.
    int ii = d2_to_d1(i, q, *n_neighbors);

    //translate neigbor number q to a real neighbor index
    int neighbor_i = neighbors[ii];

    //end of neighbor list marked by -1
    if (neighbor_i == -1) {
        h_dip[ii] = (double2)(0, 0);
        return;
    }

    double2 pos_i = pos[i];
    double2 pos_n = pos[neighbor_i];
    double2 r = pos_n - pos_i;
    double dist = length(r);

    double2 h_dip_1 = (-1. * m[neighbor_i]) / (dist*dist*dist);
    double2 h_dip_2 = (3 * r * dot(m[neighbor_i], r)) / (dist*dist*dist*dist*dist); //wtf hang: pow(dist, 5);
    double2 h_dip_i = h_dip_1 + h_dip_2;

    double my = (double)m[i].y;
    double mx = (double)m[i].x;
    double m_angle = atan2(my, mx);

    double hiy = (double)h_dip_i.y;
    double hix = (double)h_dip_i.x;
    double h_angle = atan2(hiy, hix);


    double h = length(h_dip_i);
    double theta = h_angle - m_angle;
    double h_par = h * cos(theta);
    double h_perp = h * sin(theta);
    h_dip[ii] = (double2)(h_par, h_perp);

    return;
}
