#include <CGAL/Exact_predicates_inexact_constructions_kernel.h>

#include <CGAL/Alpha_shape_3.h>
#include <CGAL/Alpha_shape_cell_base_3.h>
#include <CGAL/Alpha_shape_vertex_base_3.h>
#include <CGAL/Delaunay_triangulation_3.h>
#include <CGAL/Surface_mesh.h>
#include <fstream>
#include <list>
#include <cassert>

typedef CGAL::Exact_predicates_inexact_constructions_kernel K;
typedef CGAL::Alpha_shape_vertex_base_3<K>               Vb;
typedef CGAL::Alpha_shape_cell_base_3<K>                 Fb;
typedef CGAL::Triangulation_data_structure_3<Vb,Fb>      Tds;
typedef CGAL::Delaunay_triangulation_3<K,Tds,CGAL::Fast_location>  Delaunay;
typedef CGAL::Alpha_shape_3<Delaunay>                    Alpha_shape_3;
typedef K::Point_3                                       Point;
typedef Alpha_shape_3::Alpha_iterator                    Alpha_iterator;
typedef Alpha_shape_3::NT                                NT;
typedef Alpha_shape_3::Edge                 Edge;
typedef CGAL::Surface_mesh<Point> Mesh;

int main(int argc, char* argv[])
{
    
    if (argc != 4) {
            throw std::invalid_argument("The 1st argument: input file name\nThe 2nd argument: output file name (.off)\nThe 3rd argument: alpha value (if not positive, aptimized alpha is used)");
    }
    
    std::string input_file_name(argv[3]);
    std::string output_file_name(argv[3]);
    float alpha(std::stof(argv[3]));
    
    std::cout << input_file_name << std::endl;
    std::cout << output_file_name << std::endl;
    
    Delaunay dt;
    std::ifstream is(input_file_name);
    int n;
    is >> n;
    Point p;
    std::cout << n << " points read" << std::endl;
    for( ; n>0 ; n--) {
        is >> p;
        dt.insert(p);
    }
    std::cout << "Delaunay computed." << std::endl;
    // compute alpha shape
    Alpha_shape_3 as(dt);
    std::cout << "Alpha shape computed in REGULARIZED mode by default."
    << std::endl;
    
    if (alpha > 0) {
        
        std::cout << "Alpha value is manually assigned " << alpha << std::endl;
        as.set_alpha(alpha);

    } else {

        // find optimal alpha values
        Alpha_shape_3::NT alpha_solid = as.find_alpha_solid();
        Alpha_iterator opt = as.find_optimal_alpha(1);
        std::cout << "Smallest alpha value to get a solid through data points is "
        << alpha_solid << std::endl;
        std::cout << "Optimal alpha value to get one connected component is "
        <<  *opt    << std::endl;
        
        as.set_alpha(*opt);
        
    }
    
    assert(as.number_of_solid_components() == 1);
    
    std::vector<Alpha_shape_3::Facet> facets;
    as.get_alpha_shape_facets(std::back_inserter(facets), Alpha_shape_3::REGULAR);
    
    Mesh mesh;
    for (auto i = 0; i < facets.size(); i++) {
        
        //checks for exterior cells
        if (as.classify(facets[i].first) != Alpha_shape_3::EXTERIOR)
        {
            facets[i] = as.mirror_facet(facets[i]);
        }
        
        CGAL_assertion(as.classify(facets[i].first) == Alpha_shape_3::EXTERIOR);
        
        // gets indices of alpha shape and gets consistent orientation
        int indices[3] = { (facets[i].second + 1) % 4, (facets[i].second + 2)
            % 4, (facets[i].second + 3) % 4 };
        
        if (facets[i].second % 2 == 0) {
        
            std::swap(indices[0], indices[1]);
        }
        
        // adds data to cgal mesh
        for (auto j = 0; j < 3; ++j) {
            
            mesh.add_vertex(facets[i].first->vertex(indices[j])->point());
        }

        auto v0 = static_cast<Mesh::Vertex_index>(3 * i);
        auto v1 = static_cast<Mesh::Vertex_index>(3 * i + 1);
        auto v2 = static_cast<Mesh::Vertex_index>(3 * i + 2);
        
        mesh.add_face(v0, v1, v2);
    }

    std::ofstream output(output_file_name);
    output << mesh;
    output.close();

    return 0;
}
