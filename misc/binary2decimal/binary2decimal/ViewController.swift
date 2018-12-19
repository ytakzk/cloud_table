//
//  ViewController.swift
//  binary2decimal
//
//  Created by Yuta Akizuki on 12/13/18.
//  Copyright © 2018 ytakzk. All rights reserved.
//

import UIKit

let ON_COLOR  = UIColor(hue: 0.65, saturation: 0.9, brightness: 0.9, alpha: 1.0).cgColor
let OFF_COLOR = UIColor(hue: 0.65, saturation: 0.18, brightness: 0.9, alpha: 1.0).cgColor

class ViewController: UIViewController {

    var binaries: [Bool]     = []
    var points: [CGPoint]  = []
    var center: CGPoint = CGPoint.zero
    var lines: [CAShapeLayer] = []

    @IBOutlet weak var resetButton: UIButton!
    @IBOutlet weak var decimalLabel: UILabel!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        resetButton.setTitleColor(UIColor(cgColor: ON_COLOR), for: .normal)
        
        for _ in 0..<7 { binaries.append(false) }
    
        center = self.view.center
        
        let unitLength = self.view.frame.width * 0.3
        
        self.points = [
        
            CGPoint(x: center.x - unitLength, y: center.y - unitLength),
            CGPoint(x: center.x - unitLength, y: center.y),
            CGPoint(x: center.x - unitLength, y: center.y + unitLength),
            CGPoint(x: center.x , y: center.y  + unitLength),
            CGPoint(x: center.x + unitLength, y: center.y  + unitLength),
            CGPoint(x: center.x + unitLength, y: center.y),
            CGPoint(x: center.x + unitLength, y: center.y - unitLength),
            CGPoint(x: center.x, y: center.y  - unitLength)
        ]
    
        let pts1 = self.points.enumerated().compactMap { (offset, element) -> CGPoint? in
            
            return offset % 2 == 0 ? element : nil
        }
        
        let pts2 = self.points.shifted(by: 2).enumerated().compactMap { (offset, element) -> CGPoint? in
            
            return offset % 2 == 0 ? element : nil
        }

        for (pt1, pt2) in zip(pts1, pts2) {
            
            _ = drawLine(onLayer: self.view.layer, fromPoint: pt1, toPoint: pt2)
        }
        
        _ = drawLine(onLayer: self.view.layer,
                 fromPoint: self.points[1].center(to: self.points[7]),
                 toPoint: self.points[5].center(to: self.points[7]))
    
        _ = drawLine(onLayer: self.view.layer, fromPoint: self.points[1], toPoint: self.points[7])
        
        self.points.dropFirst(1).forEach({ (pt) in
            
            let line = drawLine(onLayer: self.view.layer, fromPoint: pt, toPoint: center)
            self.lines.append(line)
        })
        
    }
    
    @IBAction func reset(_ sender: UIButton) {
        
        self.lines.enumerated().forEach { (offset, line) in
            
            line.strokeColor = OFF_COLOR
            self.binaries[offset] = false
        }
        
        self.decimalLabel.text = "0"
    }
    
    @IBAction func tapped(_ sender: UITapGestureRecognizer) {
        
        let position = sender.location(in: self.view)
        
        var activeIndex = 0
        var smallestDist: CGFloat = 9999

        self.points.dropFirst(1).enumerated().forEach { (offset, pt) in
            
            let d = pt.center(to: self.center).distance(to: position)
            
            if d < smallestDist {
                
                smallestDist = d
                activeIndex  = offset
            }
        }
        
        let currentBinary = self.binaries[activeIndex]
        self.lines[activeIndex].strokeColor = currentBinary ? OFF_COLOR : ON_COLOR
        self.binaries[activeIndex] = !self.binaries[activeIndex]
        
        let bin = self.binaries.reversed().reduce("", { (str, binary) -> String in
            
            return "\(str)\(Int(binary ? 1 : 0))"
        })
        
        if let number = Int(bin, radix: 2) {
            
            self.decimalLabel.text = "\(number)"
        }

    }
}

private extension ViewController {
    
    func drawLine(onLayer layer: CALayer, fromPoint start: CGPoint, toPoint end: CGPoint) -> CAShapeLayer {
        
        let line        = CAShapeLayer()
        let linePath = UIBezierPath()
        linePath.move(to: start)
        linePath.addLine(to: end)
        line.path = linePath.cgPath
        line.fillColor = nil
        line.opacity = 1.0
        line.lineWidth = 1
        line.strokeColor = OFF_COLOR
        layer.addSublayer(line)
        
        return line
    }
    
}

extension CGPoint {
    
    func center(to pt: CGPoint) -> CGPoint {
        
        return CGPoint(x: (self.x + pt.x) * 0.5, y: (self.y + pt.y) * 0.5)
    }
    
    func distance(to pt: CGPoint) -> CGFloat {
        
        let xDiff = self.x - pt.x
        let yDiff = self.y - pt.y
        
        return sqrt(pow(xDiff,  2) + pow(yDiff, 2))
    }
    
}

extension Array {
    
    func shifted(by shiftAmount: Int) -> Array<Element> {
        
        guard self.count > 0, (shiftAmount % self.count) != 0 else { return self }
        
        let moduloShiftAmount = shiftAmount % self.count
        let negativeShift = shiftAmount < 0
        let effectiveShiftAmount = negativeShift ? moduloShiftAmount + self.count : moduloShiftAmount
        
        let shift: (Int) -> Int = { return $0 + effectiveShiftAmount >= self.count ? $0 + effectiveShiftAmount - self.count : $0 + effectiveShiftAmount }
        
        return self.enumerated().sorted(by: { shift($0.offset) < shift($1.offset) }).map { $0.element }
        
    }
    
}
