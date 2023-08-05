#include <cstdio>

#define cudaerr(ans) { cudaerr((ans), __FILE__, __LINE__); }
__device__ void devAssert(cudaError_t code, const char *file, int line)
{
    if (code != cudaSuccess)
    {
        printf("CUDA Err: %s %s %d\n", cudaGetErrorString(code), file, line);
    }
}

__device__ int d2_to_d1(int x, int y, int nx) {
    return x * nx + y;
}

__device__ double dotty(double2 a, double2 b) {
    return (a.x * b.x) + (a.y * b.y);
}

//Calculate the dipolar interaction from this spin(i,j)
//with all of it's neighbors.
__global__ void spin_dipolar_field(     double2 * pos,
                                        double2 * h_dip,
                                        int * neighbors,
                                        int n_neighbors,
                                        double2 * m
                                      )
{

    //this only works because i spawn a large grid and use 1-size blocks.
    int i = blockIdx.x;
    int q = blockIdx.y;


    //one thread for each neighbor.
    int ii = d2_to_d1(i, q, n_neighbors);

    //translate neigbor number q to a real neighbor index
    int neighbor_i = neighbors[ii];

    //end of neighbor list marked by -1
    if (neighbor_i == -1) {
        h_dip[ii].x = 0;
        h_dip[ii].y = 0;
        return;
    }


    double2 pos_i = pos[i];
    double2 pos_n = pos[neighbor_i];
    double2 r = {pos_n.x - pos_i.x, pos_n.y - pos_i.y};
    double dist = sqrt(r.x * r.x + r.y * r.y);

    double2 h_dip_1;
    h_dip_1.x = (-1. * m[neighbor_i].x) / pow(dist, 3);
    h_dip_1.y = (-1. * m[neighbor_i].y) / pow(dist, 3);

    double2 h_dip_2 = {0,0};
    h_dip_2.x = (3 * r.x * dotty(m[neighbor_i], r)) / pow(dist, 5);
    h_dip_2.y = (3 * r.y * dotty(m[neighbor_i], r)) / pow(dist, 5);

    double2 h_dip_i = {0,0};
    h_dip_i.x = h_dip_1.x + h_dip_2.x;
    h_dip_i.y = h_dip_1.y + h_dip_2.y;

    double my = (double)m[i].y;
    double mx = (double)m[i].x;
    double m_angle = atan2(my, mx);

    double hiy = (double)h_dip_i.y;
    double hix = (double)h_dip_i.x;
    double h_angle = atan2(hiy, hix);


    double h = sqrt(pow(h_dip_i.x, 2) + pow(h_dip_i.y, 2));
    double theta = h_angle - m_angle;
    double h_par = h * cos(theta);
    double h_perp = h * sin(theta);
    h_dip[ii].x = h_par;
    h_dip[ii].y = h_perp;

    return;
}

__global__ void external_field(char * spin, double2 * m, double2 * h_ext, double2 * tmp_ext_field, int size)
{
    int i = threadIdx.x + (blockIdx.x * blockDim.x);

    if (i >= size) {
        return;
    }


    double m_angle = atan2(spin[i] * m[i].y, spin[i] * m[i].x);

    //h_ext = self.h_ext[i]
    double h = sqrt((h_ext[i].x*h_ext[i].x + h_ext[i].y * h_ext[i].y));
    //h = norm(h_ext)
    double h_angle = atan2(h_ext[i].y, h_ext[i].x);
    //h_angle = np.arctan2(h_ext[1], h_ext[0])

    double theta = h_angle - m_angle;

    double2 h_par_perp;
    h_par_perp.x = h*cos(theta);
    h_par_perp.y = h*sin(theta);

    //double h_par = h*cos(theta);
    //double h_perp = h*sin(theta);

    tmp_ext_field[i].x = h_par_perp.x;
    tmp_ext_field[i].y = h_par_perp.y;
}

__global__ void h_dip_local(
                    double2 * h_dip_cache,
                    double alpha,
                    char * spin,
                    int * neighbors,
                    int n_neighbors,
                    double2 * ret,
                    int size)
{
    //h_dip_cache is a 2d array index on (spin, neighbor) = <num_x,num_y>

    int idx = threadIdx.x + (blockIdx.x * blockDim.x);

    if (idx >= size) {
        return;
    }

    double2 h_dip = {0, 0};
    for(int n = 0; n < n_neighbors; n++) {
        int cached_i = d2_to_d1(idx, n, n_neighbors);
        int neighbor_ii = cached_i;

        int neighbor_i = neighbors[neighbor_ii];
        if(neighbor_i == -1) {
            break;
        }

        /*
        printf("(%d, %d) neighbor num %d index %d, spin on site %d spin on neighbor: %d, cache index %d: %f, %f\\n",
                threadIdx.x,
                threadIdx.y,
                n,
                neighbor_i,
                spin[idx],
                spin[neighbor_i],
                cached_i,
                h_dip_cache[cached_i].x,
                h_dip_cache[cached_i].y);
        */

        h_dip.x += h_dip_cache[cached_i].x * spin[idx] * spin[neighbor_i];
        h_dip.y += h_dip_cache[cached_i].y * spin[idx] * spin[neighbor_i];
    }

    h_dip.x *= alpha;
    h_dip.y *= alpha;

    ret[idx] = h_dip;

}



__global__ void switching_energy_sw(
                         double2 * tmp_dip_field,
                         double2 * tmp_ext_field,
                         double2 * tmp_temp_field,
                         char * spin,
                         double * energy,
                         double b,
                         double c,
                         double beta,
                         double gamma,
                         double * thresholds,
                         int size)

{
    int i = threadIdx.x + (blockIdx.x * blockDim.x);

    if (i >= size) {
        return;
    }

    double2 h_par_perp;
    double temp_x = tmp_temp_field[i].x * spin[i];
    double temp_y = tmp_temp_field[i].y * spin[i];

    h_par_perp.x = (tmp_dip_field[i].x + tmp_ext_field[i].x + temp_x) / (b * thresholds[i]);
    h_par_perp.y = (tmp_dip_field[i].y + tmp_ext_field[i].y + temp_y) / (c * thresholds[i]);

    double e = pow(pow(h_par_perp.x, 2), (1/gamma)) + pow(pow(h_par_perp.y, 2), (1/beta)) - 1.0;
    if (h_par_perp.x >= -0.000000000012) {
        e = -(fabs(e));
    }

    energy[i] = e;
    //printf("Energy calculated: %d %f under field x direction %f\\n", i, e, tmp_ext_field[i].x);
}


// CUDA argmax reduction (basic implementation)
//
// input_array: values to be looked up with indices idx_in
// idx_in: input indices (if NULL this is assumed to level 1 and we generate them)
// idx_out: output of reduction
// size: the size of the idx_in array.

__global__ void argmax_redux(double * input_array, int *idx_in, int * idx_out, int size)
{
    extern __shared__ int sdata[];  //shared data defined outside

    unsigned int tid = threadIdx.x;
    unsigned int i = blockIdx.x * blockDim.x + threadIdx.x;  //which block * size of blocks in threads + offset

    //i is the 'absolute' index of this thread, so make sure we don't index outside of the input size.
    if (size <= i) {
        return;
    }
    //printf("I AM tid %d and blockIdx %d looking up absolute index %d with value %d\n", tid, blockIdx.x, i, idx_in[i]);

    //We got a null for indices, just use i as the index.
    if(idx_in != NULL) {
        sdata[tid] = idx_in[i]; //which index am i looking at
    } else {
        sdata[tid] = i;
    }
    __syncthreads();

    //max stride is either the block dimension, or in the case of the last block we should not stride
    //pass the size of the idx_in.
    int max_stride = blockDim.x;
    if (blockIdx.x == (blockDim.x - 1)) {
        max_stride = blockDim.x % size;
    }


    //do the per-thread reduction. note that for the last block, we do not stride outside of the array but might just compare
    //the same value twice if we go outside.
    //important for nonbuggyness: tids that are bigger than size will not run this code
    for (unsigned int stride = 1; stride < max_stride; stride *= 2) {
        if (tid % (2*stride) == 0) {
            int val_index = sdata[tid];
            int cmp_val_index = (i + stride < size) ? sdata[tid + stride] : sdata[tid];
            double val = input_array[val_index];
            double cmp_val = input_array[cmp_val_index];

            sdata[tid] = (val > cmp_val) ? val_index : cmp_val_index;
            //printf("tid %d stride %d validx %d cmpvalidx %d size %d final idx %d\n", tid, stride, val_index, cmp_val_index, size, sdata[tid]);
        }
        __syncthreads();
    }

    //Store the winning index.
    if(tid == 0) {
        idx_out[blockIdx.x] = sdata[0];
    }
}

__global__ void flip(double * swe, char * spin, int max_index, int * done, int * num_steps) {

        //printf("Flip called with maxarg %d : %f\n", max_index, swe[max_index]);
        if(swe[max_index] <= 0.0) {
            *done = 1;
        } else {
            atomicAdd(num_steps, 1); // += 1;
            spin[max_index] *= -1; //spin[max_index] *= -1;
            //printf("Step: %d Flipped %d with energy %f\n", *num_steps, max_index, swe[max_index]);
            *done = 0; //Why do I explicitly need to set this here?
        }
}

__global__ void relax(  double2 * h_dip_cache,
                        double2 * m,
                        double2 * h_ext,
                        double2 * tmp_dip_field,
                        double2 * tmp_ext_field,
                        double2 * tmp_temp_field,
                        double * thresholds,
                        double * tmp_switching_energies,
                        char * spin,
                        int * neighbors,
                        int * num_steps,
                        double  alpha,
                        double  params_b,
                        double  params_c,
                        double  params_beta,
                        double  params_gamma,
                        int  n_neighbors,
                        int  n_magnets,
                        int * done
                        )
{


    int block_size = 1024;
    int grid_size = int(1 + ceilf(n_magnets/block_size));
    //printf("Scheduling %d across grid %d with block size %d\\n", n_magnets, grid_size, block_size);

    int * argmax_idx_per_block = (int*)malloc(grid_size * sizeof(int));
    int * argmax_idx_out_final = (int*)malloc(1 * sizeof(int));

    *done = 0;

    *num_steps = 0;
    do {
        //How to calculate the switching energies:
            //calculate field energy seen by each magnet (total_fields)
                //child_kernel: full grid calculation (1 thread per magnet)

            //calculate stoner-wolfart energy for each magnet (_sw)
                //full grid calculation (1 thread per magnet)
            //cudaDeviceSynchronize()

        h_dip_local<<<grid_size, block_size>>>(h_dip_cache, alpha, spin, neighbors, n_neighbors, tmp_dip_field, n_magnets);
        external_field<<<grid_size, block_size>>>(spin, m, h_ext, tmp_ext_field, n_magnets);
        switching_energy_sw<<<grid_size, block_size>>>(tmp_dip_field, tmp_ext_field, tmp_temp_field, spin, tmp_switching_energies, params_b, params_c, params_beta, params_gamma, thresholds, n_magnets);
        cudaDeviceSynchronize();

        //Argmax Reduce the max energy flip.
        //Two levels: level 1 reduces blocks, level 2 reduces the result of blocks (stored in this-thread local memory (argmax_idx_per_block)
        //In the first reduction, the input index array is NULL, causing the kernel to generate the index based on it's absolute grid position.
        int size = n_magnets;
        argmax_redux<<<grid_size, block_size, block_size * sizeof(int)>>>(tmp_switching_energies, NULL, argmax_idx_per_block, size);
        cudaDeviceSynchronize();
        if(grid_size > 1) {
            int second_block_size = grid_size;
            //out of previous is now in
            argmax_redux<<<1, second_block_size, second_block_size * sizeof(int)>>>(tmp_switching_energies, argmax_idx_per_block, argmax_idx_out_final, second_block_size);
        } else {
            argmax_idx_out_final = argmax_idx_per_block;
        }
        cudaDeviceSynchronize();
        flip<<<1,1>>>(tmp_switching_energies, spin, *argmax_idx_out_final, done, num_steps);

    } while (*done == 0);

    if(argmax_idx_out_final != argmax_idx_per_block) {
        free(argmax_idx_out_final);
    }
    free(argmax_idx_per_block);

    //for(int q = 0; q < n_magnets; q++) {
    //    printf("Spins when I am done: %d\\n", spin[q]);
    //}
}
