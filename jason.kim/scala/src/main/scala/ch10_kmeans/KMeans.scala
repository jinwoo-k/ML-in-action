package ch10_kmeans

import ch10_kmeans.KMeans.ClusterAssignment

import scala.io.Source
import scala.util.Random

object KMeans {
  type Row[T] = Array[T]
  type Col[T] = Array[T]
  type Matrix[T] = Row[Col[T]]
  type DistCalcMethod = (Row[Double], Row[Double]) => Double
  type CreateCenterMethod = (Matrix[Double], Int) => Matrix[Double]

  def loadDataSet(filename: String): Matrix[Double] =
    Source.fromFile(filename).getLines.map(parseLine).toArray

  def parseLine(line: String): Row[Double] =
    line.split("\t").map(_.toDouble)

  def getEuclidDist(r1: Row[Double], r2: Row[Double]): Double =
    Math.sqrt(r1.zip(r2).map{ case (e1, e2) => Math.pow(e1 - e2, 2) }.sum)

  def getRandomCentroids(dataSet: Matrix[Double], k: Int): Matrix[Double] = {
    val rangeRow = for {
      colNum <- dataSet(0).indices
    } yield {
      val colVector = dataSet.map(row => row(colNum))
      (colVector.min, colVector.max)
    }

    Range(0, k).map(_ => getRandomCentroid(rangeRow.toArray)).toArray
  }

  def getRandomCentroid(rangeArr: Row[(Double, Double)]): Row[Double] =
    rangeArr.map{ case (min, max) => min + ((max - min) * Random.nextDouble())}

  def kMeans(
      dataSet: Matrix[Double],
      k: Int,
      calcDist: DistCalcMethod = getEuclidDist,
      createCenter: CreateCenterMethod = getRandomCentroids
    ): (Matrix[Double], Row[ClusterAssignment]) = {

    def loop(centroids: Matrix[Double]): (Matrix[Double], Row[ClusterAssignment]) = {
      val clusterAssignments = dataSet.map(row => {
          val (index, dist) = centroids.indices.map(i => {
              (i, getEuclidDist(row, centroids(i)))
            }).minBy(_._2)
          ClusterAssignment(index, dist)
        })

      val newCentroids = centroids.indices.map(i => {
        val dataSetInCentroids = dataSet.zip(clusterAssignments).filter(_._2.index == i).map(_._1)
        calcMeanByColumn(dataSetInCentroids)
      }).toArray

      if (centroids.deep == newCentroids.deep) {
        (centroids, clusterAssignments)
      } else {
        loop(newCentroids)
      }
    }

    val centroids = createCenter(dataSet, k)
    loop(centroids)
  }

  def calcMeanByColumn(dataSet: Matrix[Double]): Row[Double] = {
    dataSet(0).indices.map(i => {
      val cols = dataSet.map(_(i))
      cols.sum / cols.length
    }).toArray
  }

  def biKMeans(
      dataSet: Matrix[Double],
      k: Int,
      calcDist: DistCalcMethod = getEuclidDist,
      createCenter: CreateCenterMethod = getRandomCentroids
    ): (Matrix[Double], Row[ClusterAssignment]) = {
    // TODO
  }




  def main(args: Row[String]): Unit = {
    val dataMat = loadDataSet("/Users/jason.kim/Study/ML/ML-in-action/jason.kim/code/ch10.k_means_clustering/testSet.txt")
    dataMat(0).indices.foreach(i => {
      val col = dataMat.map(row => row(i))
      println(s"colNum: $i, min: ${col.min}, max: ${col.max}")
    })

    val (centroids, clusterAssignments) = kMeans(dataMat, 4)
    centroids.foreach(c => println(c.mkString(", ")))
    clusterAssignments.foreach(println)
  }


  case class ClusterAssignment(index: Int, squaredDist: Double)


}
