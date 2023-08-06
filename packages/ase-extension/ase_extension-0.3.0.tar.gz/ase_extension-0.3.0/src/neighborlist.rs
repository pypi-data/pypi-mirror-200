use gchemol_neighbors::{Neighbor, Neighborhood};
use rayon::prelude::*;

pub struct NeighborList {
    pub idx_i: Vec<usize>,
    pub idx_j: Vec<usize>,
    pub dists: Vec<f64>,
    pub offsets: Vec<[f64; 3]>,
}

pub fn construct_neighbor_list(
    points: &[[f64; 3]],
    cell: Option<&[[f64; 3]; 3]>,
    cutoff: f64,
    parallel: bool,
) -> NeighborList {
    let mut nh = Neighborhood::new();
    nh.update(points.iter().enumerate().map(|(i, &v)| (i, v)));
    if let Some(cell) = cell {
        nh.set_lattice(*cell);
    }
    let n = points.len();

    let neighbors_all: Vec<Vec<Neighbor>> = match parallel {
        true => (0..n)
            .into_par_iter()
            .take(n)
            .map(|i| nh.neighbors(i, cutoff).collect::<Vec<Neighbor>>())
            .collect(),
        false => (0..n)
            .take(n)
            .map(|i| nh.neighbors(i, cutoff).collect::<Vec<Neighbor>>())
            .collect(),
    };

    let mut idx_i: Vec<usize> = vec![];
    let mut idx_j: Vec<usize> = vec![];
    let mut dists: Vec<f64> = vec![];
    let mut offsets: Vec<[f64; 3]> = vec![];

    for (i, neighbors) in neighbors_all.iter().enumerate() {
        for neighbor in neighbors {
            idx_i.push(i);
            idx_j.push(neighbor.node);
            dists.push(neighbor.distance);
            let offset = match neighbor.image {
                Some(image) => [image[0], image[1], image[2]],
                None => [0.0, 0.0, 0.0],
            };
            offsets.push(offset);
        }
    }
    NeighborList {
        idx_i,
        idx_j,
        dists,
        offsets,
    }
}
