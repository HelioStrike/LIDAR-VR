using System;
using System.IO;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PointCloudRenderer : MonoBehaviour {

	public string path;
	public int numX, numY, numZ;
	public Material mat;
	public Shader shader;

	// Use this for initialization
	void Start () {
		string[] lines = File.ReadAllLines(path);
		
		int[,,] point_bins = new int[numX+1,numY+1,numZ+1];
		for(int i = 0; i < numX; i++)
		{
			for(int j = 0; j < numY; j++)
			{
				for(int k = 0; k < numZ; k++)
				{
					point_bins[i,j,k] = 0;
				}
			}
		}

		int inf = 99999999;
		float currX,currY,currZ,minX=inf,minY=inf,minZ=inf,maxX=-inf,maxY=-inf,maxZ=-inf;
		int totPoints = int.Parse(lines[1].Split(' ')[0]);
		for(int i = 2; i < totPoints+2; i++)
		{
			string[] divs = lines[i].Split(' ');
			
			currX = float.Parse(divs[0]);
			currY = float.Parse(divs[1]);
			currZ = float.Parse(divs[2]);

			if(currX < minX) minX = currX;
			if(currX > maxX) maxX = currX;

			if(currY < minY) minY = currY;
			if(currY > maxY) maxY = currY;

			if(currZ < minZ) minZ = currZ;
			if(currZ > maxZ) maxZ = currZ;
		} 

		float diffX = Math.Abs(minX - maxX);
		float diffY = Math.Abs(minY - maxY);
		float diffZ = Math.Abs(minZ - maxZ);

		int numPoints = 0;

		for(int i = 2; i < totPoints+2; i++)
		{
			string[] divs = lines[i].Split(' ');
			
			currX = numX*(float.Parse(divs[0]) - minX)/diffX;
			currY = numY*(float.Parse(divs[1]) - minY)/diffY;
			currZ = numZ*(float.Parse(divs[2]) - minZ)/diffZ;

			if(point_bins[(int)currX,(int)currY,(int)currZ] == 0) { numPoints++;}
			
			point_bins[(int)currX,(int)currY,(int)currZ] = 1;
		} 

		int curr = 0;
		Vector3[] points = new Vector3[numPoints];
		
		for(int i = 0; i < numX; i++)
		{
			for(int j = 0; j < numY; j++)
			{
				for(int k = 0; k < numZ; k++)
				{
					if(point_bins[i,j,k] == 1)
					{
						points[curr] = new Vector3(i*diffX/diffZ, j*diffY/diffZ, k);
						curr++;
					}
				}
			}
		}

		Vector2[] uvs = new Vector2[points.Length];
		Color[] colors = new Color[points.Length];
		for(int i = 0; i < points.Length; i++)
		{
			uvs[i] = new Vector2(points[i].x, points[i].z);
			colors[i] = Color.red;
		}

		gameObject.AddComponent<MeshFilter>();
		gameObject.AddComponent<MeshRenderer>();
 		mat.shader = shader;
		this.GetComponent<MeshRenderer>().material = mat;
	    Mesh mesh = GetComponent<MeshFilter>().mesh;


		Debug.Log(points.Length);

		mesh.vertices = points;
		mesh.uv = uvs;
		mesh.colors = colors;
	}
	
	// Update is called once per frame
	void Update () {

	}	
}
