#include <CGAL/Exact_predicates_inexact_constructions_kernel.h>

#include <CGAL/Alpha_shape_3.h>
#include <CGAL/Alpha_shape_cell_base_3.h>
#include <CGAL/Alpha_shape_vertex_base_3.h>
#include <CGAL/Delaunay_triangulation_3.h>
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

int main(int argc, char* argv[]) 
{

    if (argc != 3) {
        throw std::invalid_argument("The 1st argument: input file name\nThe 2nd argument: output file name (.off)");
    }

    std::string input_file_name(argv[1]);
    std::string output_file_name(argv[2]);

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
    std::cout << "Alpha shape computed in REGULARIZED mode by defaut."
    << std::endl;
    // find optimal alpha values
    Alpha_shape_3::NT alpha_solid = as.find_alpha_solid();
    Alpha_iterator opt = as.find_optimal_alpha(1);
    std::cout << "Smallest alpha value to get a solid through data points is "
    << alpha_solid << std::endl;
    std::cout << "Optimal alpha value to get one connected component is "
    <<  *opt    << std::endl;
    as.set_alpha(*opt);
    assert(as.number_of_solid_components() == 1);
    
    std::vector<Alpha_shape_3::Facet> facets;
    as.get_alpha_shape_facets(std::back_inserter(facets), Alpha_shape_3::REGULAR);
    
    std::stringstream pts;
    std::stringstream ind;
    
    std::size_t nbf=facets.size();
    for (std::size_t i=0;i<nbf;++i)
    {
        //To have a consistent orientation of the facet, always consider an exterior cell
        if ( as.classify( facets[i].first )!=Alpha_shape_3::EXTERIOR )
            facets[i]=as.mirror_facet( facets[i] );
        CGAL_assertion(  as.classify( facets[i].first )==Alpha_shape_3::EXTERIOR  );
        
        int indices[3]={
            (facets[i].second+1)%4,
            (facets[i].second+2)%4,
            (facets[i].second+3)%4,
        };
        
        /// according to the encoding of vertex indices, this is needed to get
        /// a consistent orienation
        if ( facets[i].second%2==0 ) std::swap(indices[0], indices[1]);
        
        
        pts <<
        facets[i].first->vertex(indices[0])->point() << "\n" <<
        facets[i].first->vertex(indices[1])->point() << "\n" <<
        facets[i].first->vertex(indices[2])->point() << "\n";
        ind << "3 " << 3*i << " " << 3*i+1 << " " << 3*i+2 << "\n";
    }
    
    // std::cout << "OFF "<< 3*nbf << " " << nbf << " 0\n";
    // std::cout << pts.str();
    // std::cout << ind.str();

    
    std::ofstream output_file;
    output_file.open (output_file_name);
    output_file << "OFF\n"<< 3*nbf << " " << nbf << " 0\n";
    output_file << pts.str();
    output_file << ind.str();
    output_file.close();

    return 0;
}
